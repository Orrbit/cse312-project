# This is where the routes are defined.
from flask import Blueprint, flash, Markup, redirect, render_template, url_for, request, jsonify, escape, send_from_directory
from werkzeug.utils import secure_filename
from biazza import app
import os


import json, run

# Socket.io stuffio
from flask_socketio import SocketIO, send, emit

socketio = SocketIO(app)

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


# Socket stuff

likes = 0 # going to be an array/dictionary when we make it for new users

@socketio.on('connect') # when socket connects
def on_connect():
   print('Socket Connected')

   likes = run.globalLikes # assign global likes to this environment likes

   print('initial likes : ' + str(likes))

   emit('initialUpdate', {'id_name' : '<enter identifier>', 'number': likes})

@socketio.on('disconnect') # when socket dis-connects
def on_disconnect():
   print('Socket Disconnected')
   # emit('initialUpdate', {'id_name' : '<enter identifier>', 'number': likes}) probably put a emit message for disconnection as well

@socketio.on('message')
def handle_message(message):
   incoming_message = str(message)

   print('Received message : ' + incoming_message + ' Likes : ' + str(message["number"]) + ' globalLikes : ' + str(run.globalLikes)) # receiving JSON data

   # probably make this such that it works specific to the message identifier.

   run.globalLikes = message["number"]
   likes = run.globalLikes

   emit('updateCount', message, broadcast = True) # BroadCast message to all clients

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

