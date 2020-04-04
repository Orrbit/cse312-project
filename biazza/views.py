# This is where the routes are defined.
from flask import Blueprint, flash, Markup, redirect, render_template, url_for, request, jsonify, escape, send_from_directory
from werkzeug.utils import secure_filename
from biazza import app
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

@app.route('/home/questions/files', methods=['POST'])
def upload_file_to_question():
   file = request.files['file']
   filename = secure_filename(file.filename)
   filename = escape(filename)
   file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

   return jsonify({'filename': filename, 'href': '/home/questions/files/'+filename})

@app.route('/home/questions/files/<string:filename>')
def return_file(filename):
   return send_from_directory(app.config['UPLOAD_FOLDER'], filename)