# This is where the routes are defined.
from flask import Blueprint, flash, Markup, redirect, render_template, url_for, request, Response, jsonify, escape, \
    send_from_directory, send_file, make_response
from werkzeug.utils import secure_filename
# from biazza.database import db_session
from biazza import app, ALLOWED_EXTENSIONS
from biazza.models import Attachment, Comment, Question, Accounts, Conversation, Message, db
from sqlalchemy.orm import aliased
from sqlalchemy import or_, join, not_, and_
from biazza.socket_handlers import emit_comment, emit_question
from biazza.room_handlers import emit_message
from biazza.token_util import create_token_for_user, table_contains_token, get_user_with_token, delete_token
import os
import uuid
import bcrypt
import re
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'GET':
        print("IN GET")
        token = request.cookies.get('biazza_token')
        print(token)
        if token and get_user_with_token(token):
            return redirect('/home')
        return render_template("login.html")
    
    else:
        form_data = request.form

        email = form_data.get("email")
        password = form_data.get("password")

        email = replace(email)
        password = replace(password)

        password = password.encode('utf-8')

        # verify that the user is present in the database if not present stay, else go to the home page

        emails_query = Accounts.query.filter_by(email = email).first()

        if emails_query is None:
            return jsonify("email_not_found")
        else:

            # check if the password is valid Abcdef1!
            stored_password = emails_query.password
            stored_password = stored_password.encode('utf-8')

            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            if bcrypt.checkpw(password, stored_password):
                token = create_token_for_user(emails_query.id)
                response = make_response(jsonify("Success"))
                response.set_cookie('biazza_token', token)
                return response
            else:
                return jsonify("invalid_password")


@app.route('/signup', methods=['GET', 'POST'])
def handle_signup():

    # print("WHERE TF YOU AT")
    # print(request.form)

    if request.method == 'GET':
        return send_file('static/signup.html')
    else:
        # This part will handle validation of signup requests

        form_data = request.form 

        email = form_data.get("email")
        first_name = form_data.get("firstName")
        last_name = form_data.get("lastName")
        password = form_data.get("password")

        # check password strength. Conditions to check. Size >= 8, One big char, One number, One special char
        check_size = (len(password) >= 8)
        check_cap  = True
        check_num  = True
        check_spec = True
        check_lower = True

        # check upper case char
        if not any(x.isupper() for x in password):
            check_cap = False

        if not any(x.islower() for x in password):
            check_lower = False
        
        # check number
        if not any(x.isdigit() for x in password):
            check_num = False

        # check special char
        string_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]') 
        if(string_check.search(password) == None):
            check_spec = False

        # return a json string
        if((check_size and check_cap and check_num and check_spec) == False):
            return jsonify({"size" : check_size, "cap" : check_cap, "num" : check_num, "spec" : check_spec, "lower": check_lower})

        # change all emails for Injection
        email = replace(email)
        first_name = replace(first_name)
        last_name = replace(last_name)
        password = replace(password)

        print(password)
        # hash the password
        password = password.encode('utf-8')
        password = bcrypt.hashpw(password, bcrypt.gensalt())

        # check with database if email is taken.
        emails_query = Accounts.query.filter_by(email = email).first()

        # if not taken, use bcrypt to hasha + salt the password
        if emails_query is None:
            print("EMAIL NOT FOUND")

            # insert the user data into the mySQL table
            # store the new email + rest in the data base
            to_insert = Accounts(email = email, first_name = first_name, last_name = last_name, password = password)
            result = db.session.add(to_insert)
            db.session.commit()

            uid = to_insert.id
            token = create_token_for_user(uid)

            response = make_response(jsonify("Success"))
            response.set_cookie('biazza_token', token)
            return response
        # if taken, send message to user that the email is taken
        else:
            print("EMAIL FOUND")
            
            # send invalid or error request to the client
            return jsonify("email_found")



@app.route('/home')
def home_page():
    token = request.cookies.get('biazza_token')
    user = get_user_with_token(token)

    # If the user could not be found in the db make them login
    if not user:
        return render_template("login.html")

    users_name = user.first_name + ' ' + user.last_name
    # We now have info about the user and can put their info in the top right
    return render_template('home.html', name=users_name)


@app.route('/home/messages')
def messages():
    token = request.cookies.get('biazza_token')
    user = get_user_with_token(token)

    # If the user could not be found in the db make them login
    if not user:
        return render_template("login.html")

    # Getting the conversations for the side bar

    conversation_summary = get_users_conversation_bar(user.id)


    users_to_start_conversation = Accounts.query.filter(Accounts.id != user.id)

    messages_of_top_conversation = []
    if conversation_summary:
        messages_of_top_conversation = get_all_messages_of_conversation(conversation_summary[0]["id"], user.id)

    return render_template('messages.html', potential_conversation_users=users_to_start_conversation,
                                            conversations_with_all=conversation_summary,
                                            messages_of_top_conversation=messages_of_top_conversation,
                                            uid=user.id)

def get_users_conversation_bar(uid):
    rv = []
    conversations_with_guests = Conversation.query\
        .join(Accounts, Conversation.user_guest_id == Accounts.id) \
        .add_columns(Conversation.id, Accounts.first_name, Accounts.last_name)\
        .filter(Conversation.user_owner_id == uid)
    conversations_with_hosts = Conversation.query\
        .join(Accounts, Conversation.user_owner_id == Accounts.id) \
        .add_columns(Conversation.id, Accounts.first_name, Accounts.last_name)\
        .filter(Conversation.user_guest_id == uid)
    conversations_with_all_query = conversations_with_guests.union(conversations_with_hosts)
    num_conv = conversations_with_all_query.count()
    conversations_with_all = conversations_with_all_query

    for conversation in conversations_with_all:
        header_message = Message.query \
            .filter(Message.conversation_id == conversation[0].id) \
            .order_by(Message.time.desc()) \
            .first()
        msg = ""
        time = ""
        if header_message:
            msg = header_message.text
            time = header_message.time
        conversation_header_obj = {
            "name": conversation[2] + conversation[3], 
            "id": conversation[0].id, 
            "account_id": conversation[1], 
            "highlight_message": msg, 
            "highlight_message_date": time
        }
        rv.append(conversation_header_obj)
    return rv

def get_all_messages_of_conversation(cid, uid):
    rv = []
    messages = Conversation.query\
        .join(Message, Conversation.id == Message.conversation_id) \
        .join(Accounts, Accounts.id == Message.sender_id) \
        .add_columns(Accounts.id==uid, Message.text, Message.time, Accounts.first_name, Accounts.last_name) \
        .filter(Conversation.id == cid) \
        .order_by(Message.time)\
        .all()
    for m in messages:
        rv.append({
            "is_me":m[1],
            "text":m[2],
            "time":m[3],
            "name":m[4]+m[5]
        })
    return rv

@app.route('/message', methods=['POST', 'GET'])
def messagesCRUD():
    token = request.cookies.get('biazza_token')
    user = get_user_with_token(token)

    # If the user could not be found in the db make them login
    if not user:
        return Response(status=404)
    
    if request.method == 'POST':
        text = request.form['text']
        conversation_id = request.form['conversation_id']
        time = datetime.now()
        text = request.form['text']

        message = Message(conversation_id=conversation_id, text=text, time=time, sender_id=user.id)
        db.session.add(message)
        db.session.commit()

        account_sender = Accounts.query.filter(Accounts.id == user.id).first()
        name_of_sender = account_sender.first_name + ' ' + account_sender.last_name

        emit_message(conversation_id, message, name_of_sender)

        return Response(status=200)

@app.route('/conversation', methods=['GET', 'POST'])
def conversationsCRUD():
    token = request.cookies.get('biazza_token')
    user = get_user_with_token(token)

    # If the user could not be found in the db make them login
    if not user:
        return Response(status=404)

    if request.method == 'GET':
        conversation_id = request.args['conversation_id']
        conversation = Conversation.query.filter(Conversation.id == conversation_id).first()
        if not conversation:
            return Response(status=404)

        data = get_all_messages_of_conversation(conversation_id, user.id)
        return jsonify(data)

    elif request.method == 'POST':
        user_guest_id = request.form['guest_user']
        conversation = Conversation(user_owner_id=user.id, user_guest_id=user_guest_id)
        db.session.add(conversation)
        db.session.commit()
        return jsonify({
            "id":conversation.id
        })


@app.route('/home/questions', methods=['GET', 'POST'])
def questions():
    if request.method == 'GET':

        token = request.cookies.get('biazza_token')
        user = get_user_with_token(token)

        # If the user could not be found in the db make them login
        if not user:
            return render_template("login.html")

        questions = Question.query.all()
        questions.reverse()

        top_question = None
        comments = []

        if questions:
            top_question = questions[0]
            comments = Comment.query.filter(Comment.question_id == top_question.id)

            top_question_poster = Accounts.query.filter(Accounts.id == top_question.user_id).first()
            top_question.user_name = top_question_poster.first_name + ' ' + top_question_poster.last_name

        for c in comments:
            c.all_attachments = Attachment.query.filter(Attachment.comment_id == c.id)
            comment_poster = Accounts.query.filter(Accounts.id == c.user_id).first()
            c.user_name = comment_poster.first_name + ' ' + comment_poster.last_name
        return render_template('questions.html', comments=comments, questions=questions, top_question=top_question)

    elif request.method == 'POST':

        token = request.cookies.get('biazza_token')
        user = get_user_with_token(token)

        # If the user could not be found in the db make them login
        if not user:
            return render_template("login.html")

        question_title = replace(request.form['title-input'])
        question_contents = replace(request.form['question-input'])

        if len(question_title) > 0 and len(question_contents) > 0:
            # Need to handle file uploads and clean input from users
            question = Question(title=question_title, content=question_contents, likes=0, user_id=user.id)
            db.session.add(question)
            db.session.commit()
            emit_question(question, [])
            return jsonify({'success': True})
        else:
            return Response(status=400)

@app.route('/home/questions/<int:q_id>')
def get_question(q_id):
    token = request.cookies.get('biazza_token')
    user = get_user_with_token(token)

    # If the user could not be found in the db make them login
    if not user:
        return render_template("login.html")

    try:
        q = Question.query.filter(Question.id == q_id).one()
    except:
        return Response(status=404)

    poster = Accounts.query.filter(Accounts.id == q.user_id).first()
    q.user_name = poster.first_name + ' ' + poster.last_name

    comments = Comment.query.filter(Comment.question_id == q_id)
    comments_json = []
    for c in comments:
        c.all_attachments = Attachment.query.filter(Attachment.comment_id == c.id)
        comment_poster = Accounts.query.filter(Accounts.id == c.user_id).first()
        c.user_name = comment_poster.first_name + ' ' + comment_poster.last_name

        attachments_json = []
        for a in c.all_attachments:
            a = {
                "path": a.path,
                "name": a.user_filename
            }
            attachments_json.append(a)
        c.all_attachments = attachments_json
        comments_json.append({
            'c_id': c.id,
            'c_text': c.text,
            'c_likes': c.likes,
            'attachments': c.all_attachments,
            'name': c.user_name
        })

    return jsonify({
        'id': q_id,
        'name': q.user_name,
        'title': q.title,
        'content': q.content,
        'likes': q.likes,
        'comments': comments_json
    })


@app.route('/home/assignments')
def assignments():
    token = request.cookies.get('biazza_token')
    user = get_user_with_token(token)

    # If the user could not be found in the db make them login
    if not user:
        return render_template("login.html")

    return render_template('assignments.html')


def replace(text):
    text = text.replace(">", "&gt;")
    text = text.replace("<", "&lt;")
    text = text.replace("&", "&amp;")

    return text


# Used for sending the comment send form to the server
@app.route('/home/questions/<int:q_id>/comments', methods=['POST'])
def post_comment_to_question(q_id):
    token = request.cookies.get('biazza_token')
    user = get_user_with_token(token)

    # If the user could not be found in the db make them login
    if not user:
        return render_template("login.html")

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    form_text = request.form['comment-string']

    form_text = replace(form_text)

    print(form_text)

    comment = Comment(text=form_text, likes=0, question_id=q_id, user_id=user.id)

    #  msg = msg.replace(">","&gt;"); msg = msg.replace("<","&lt;"); msg = msg.replace("&", "&amp;");
    #  </div><script>alert('PeePeePooPoo');</script>

    db.session.add(comment)
    db.session.commit()

    attachments = []
    for file in request.files.getlist('attachments-input'):
        if file.filename != '':
            client_file_name = escape(secure_filename(file.filename))
            extension = os.path.splitext(client_file_name)[1]
            server_file_name = uuid.uuid4().hex + extension
            server_path = os.path.join(app.config['UPLOAD_FOLDER'], server_file_name)
            href_path = remove_prefix(server_path, "/app/biazza/static")
            attachment = Attachment(user_filename=client_file_name, path=href_path, comment_id=comment.id)
            db.session.add(attachment)
            db.session.commit()
            attachments.append(attachment)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], server_file_name))
            print("Attachment saved: " + repr(attachment))
    emit_comment(comment, attachments)
    return jsonify({'success': True})


@app.route('/logout')
def handle_logout():
    token = request.cookies.get('biazza_token')
    delete_token(token)
    return render_template('login.html')


# when a connection closes, the db session will also close
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def remove_prefix(s, prefix):
    return s[len(prefix):] if s.startswith(prefix) else s
