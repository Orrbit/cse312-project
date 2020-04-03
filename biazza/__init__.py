from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

UPLOAD_FOLDER = '/app/biazza/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object('config')

socketio = SocketIO(app)

import biazza.views
import biazza.socket_handlers