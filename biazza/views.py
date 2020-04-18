# This is where the routes are defined.
from flask import Blueprint, flash, Markup, redirect, render_template, url_for, request, Response, jsonify, escape, send_from_directory
from werkzeug.utils import secure_filename
#from biazza.database import db_session
from biazza import app, ALLOWED_EXTENSIONS
from biazza.models import Attachment, Comment, Question, db
from biazza.socket_handlers import emit_comment, emit_question
import os
import uuid


@app.route('/')
def home():
   return render_template("login.html")

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
         return jsonify({'success':True})
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

#Used for sending the comment send form to the server
@app.route('/home/questions/<int:q_id>/comments', methods=['POST'])
def post_comment_to_question(q_id):
   if not os.path.exists(app.config['UPLOAD_FOLDER']):
      os.makedirs(app.config['UPLOAD_FOLDER'])
   
   form_text = request.form['comment-string']

   form_text  = replace(form_text)

   print(form_text)
   
   comment = Comment(text=form_text, likes=0, question_id=q_id)

#  msg = msg.replace(">","&gt;"); msg = msg.replace("<","&lt;"); msg = msg.replace("&", "&amp;");
#  </div><script>alert('PeePeePooPoo');</script>

   db.session.add(comment)
   db.session.commit()

   attachments=[]
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
   return jsonify({'success':True}) 

#when a connection closes, the db session will also close
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_prefix(s, prefix):
   return s[len(prefix):] if s.startswith(prefix) else s
