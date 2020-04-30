# This is where the routes are defined.
from flask import Blueprint, flash, Markup, redirect, render_template, url_for, request, Response, jsonify, escape, \
    send_from_directory, send_file, make_response
from werkzeug.utils import secure_filename
# from biazza.database import db_session
from biazza import app, ALLOWED_EXTENSIONS
from biazza.models import Attachment, Comment, Question, Accounts, db
from biazza.socket_handlers import emit_comment, emit_question
from biazza.token_util import create_token_for_user, table_contains_token
import os
import uuid
import bcrypt
import re

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'GET':
        print("IN GET")
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

            if(bcrypt.checkpw(password, stored_password)):
                return jsonify("Success")
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

        # check upper case char
        if not any(x.isupper() for x in password):
            check_cap = False
        
        # check number
        if not any(x.isdigit() for x in password):
            check_num = False

        # check special char
        string_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]') 
        if(string_check.search(password) == None):
            check_spec = False

        # return a json string
        if((check_size and check_cap and check_num and check_spec) == False):
            return jsonify({"size" : check_size, "cap" : check_cap, "num" : check_num, "spec" : check_spec})

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
    return render_template('home.html')


@app.route('/home/messages')
def messages():
    return render_template('messages.html')


@app.route('/home/questions', methods=['GET', 'POST'])
def questions():
    if request.method == 'GET':

        questions = Question.query.all()
        questions.reverse()

        top_question = None
        comments = []

        if questions:
            top_question = questions[0]
            comments = Comment.query.filter(Comment.question_id == top_question.id)

        for c in comments:
            c.all_attachments = Attachment.query.filter(Attachment.comment_id == c.id)
        return render_template('questions.html', comments=comments, questions=questions, top_question=top_question)

    elif request.method == 'POST':
        question_title = replace(request.form['title-input'])
        question_contents = replace(request.form['question-input'])

        if len(question_title) > 0 and len(question_contents) > 0:
            # Need to handle file uploads and clean input from users
            question = Question(title=question_title, content=question_contents, likes=0)
            db.session.add(question)
            db.session.commit()
            emit_question(question, [])
            return jsonify({'success': True})
        else:
            return Response(status=400)


@app.route('/home/questions/<int:q_id>')
def get_question(q_id):
    try:
        q = Question.query.filter(Question.id == q_id).one()
    except:
        return Response(status=404)

    comments = Comment.query.filter(Comment.question_id == q_id)
    for c in comments:
        c.all_attachments = Attachment.query.filter(Attachment.comment_id == c.id)

        attachments_json = []
        for a in c.all_attachments:
            a = {
                "path": a.path,
                "name": a.user_filename
            }
            attachments_json.append(a)
        c.all_attachments = attachments_json

    comments_json = []
    for comment in comments:
        comments_json.append({
            'c_id': comment.id,
            'c_text': comment.text,
            'c_likes': comment.likes,
            'attachments': comment.all_attachments
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
    return render_template('assignments.html')


def replace(text):
    text = text.replace(">", "&gt;")
    text = text.replace("<", "&lt;")
    text = text.replace("&", "&amp;")

    return text


# Used for sending the comment send form to the server
@app.route('/home/questions/<int:q_id>/comments', methods=['POST'])
def post_comment_to_question(q_id):
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    form_text = request.form['comment-string']

    form_text = replace(form_text)

    print(form_text)

    comment = Comment(text=form_text, likes=0, question_id=q_id)

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


# when a connection closes, the db session will also close
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def remove_prefix(s, prefix):
    return s[len(prefix):] if s.startswith(prefix) else s
