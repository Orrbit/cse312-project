# run.py
#!/usr/bin/env python
from biazza import app, socketio
import eventlet
eventlet.monkey_patch()

globalLikes = {} # Probably going to keep track of all the likes. But will probably be a dictionary

if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port=8000)
    socketio.run(app, port=8000, host='0.0.0.0', debug=True, log_output=True)