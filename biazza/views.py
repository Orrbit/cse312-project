# This is where the routes are defined.
from flask import Blueprint, flash, Markup, redirect, render_template, url_for
from biazza import app

@app.route('/')
def home():
   return "hello world, biazza!"