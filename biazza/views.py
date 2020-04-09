# This is where the routes are defined.
from flask import Blueprint, flash, Markup, redirect, render_template, url_for, request, jsonify, escape, send_from_directory
from werkzeug.utils import secure_filename
#from biazza.database import db_session
from biazza import app, ALLOWED_EXTENSIONS
from biazza.models import Attachment, Comment, db
from biazza.socket_handlers import emit_comment
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

@app.route('/home/questions')
def questions():
   comments = Comment.query.all()
   for c in comments:
      c.all_attachments = Attachment.query.filter(Attachment.comment_id == c.id)
   return render_template('questions.html', comments=comments)

@app.route('/home/assignments')
def assignments():
   return render_template('assignments.html')

#Used for sending the comment send form to the server
@app.route('/home/questions/comments', methods=['POST'])
def post_comment_to_question():
   if not os.path.exists(app.config['UPLOAD_FOLDER']):
      os.makedirs(app.config['UPLOAD_FOLDER'])
   
   form_text = request.form['comment-string']
   comment = Comment(text=form_text, likes=0)
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
