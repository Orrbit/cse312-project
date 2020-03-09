# This is where the routes are defined.
from flask import Blueprint, flash, Markup, redirect, render_template, url_for
from biazza import app

@app.route('/')
def home():
   return "hello world, biazza!"


@app.route('/home')
def home_page():
   return app.send_static_file('index.html')


@app.route('/home/messages')
def messages():
   return app.send_static_file('messages.html')


@app.route('/css/messages')
def messages_css():
   return app.send_static_file('messages.css')


@app.route('/css/home')
def home_css():
   return app.send_static_file('index.css')
