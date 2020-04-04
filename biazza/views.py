# This is where the routes are defined.
from flask import Blueprint, flash, Markup, redirect, render_template, url_for
from biazza import app

# Socket.io stuffio
from flask_socketio import SocketIO

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

