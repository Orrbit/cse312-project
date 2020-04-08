from flask import Flask
from flask_socketio import SocketIO
import flask_sqlalchemy

from biazza.models import db


app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

UPLOAD_FOLDER = '/app/biazza/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@db:3306/biazza'
app.config.from_object('config')
app.app_context().push()

db.init_app(app)
db.create_all()
socketio = SocketIO(app)

import biazza.views
import biazza.models
import biazza.socket_handlers