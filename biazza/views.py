# This is where the routes are defined.
from flask import Blueprint, flash, Markup, redirect, render_template, url_for, request, jsonify, escape, send_from_directory
from werkzeug.utils import secure_filename
#from biazza.database import db_session
from biazza import app, ALLOWED_EXTENSIONS
from biazza.models import Attachment, Comment, db
import os


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
   return render_template('questions.html')

@app.route('/home/assignments')
def assignments():
   return render_template('assignments.html')


@app.route('/home/questions/comments', methods=['POST'])
def post_comment_to_question():
   # Eventually there needs to be some form of identifier included for the question that it is in response to
   # Get comment with request.get_data('comment-string')
   # Loop through files with request.files


   #socket emit to all listeners


#### WILL DELETE
@app.route('/home/questions/files', methods=['POST'])
def upload_file_to_question():
   if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
   file = request.files['file']
   if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
   if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      filename = escape(filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      path_for_file = '/home/questions/files/'+filename
      attachment = Attachment(filename=filename, path=path_for_file)
      db.session.add(attachment)
      db.session.commit()
      comment = Comment(text="Hello World", attachment_id=1, likes=1)
      db.session.add(comment)
      db.session.commit()
      

      return jsonify({'filename': filename, 'href': path_for_file})
   

@app.route('/home/questions/files/<string:filename>')
def return_file(filename):
   return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#when a connection closes, the db session will also close
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
