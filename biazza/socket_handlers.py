from biazza import socketio
from flask_socketio import emit
import lxml.html, lxml.html.clean
import run


@socketio.on('question_comment')
def question_comment(data):
    print('Received:', data)
    comment = data['comment']
    comment_html = lxml.html.fromstring(comment)
    comment_html = lxml.html.clean.clean_html(comment_html)
    comment_html = lxml.html.tostring(comment_html)
    print('Cleaned:', comment_html.decode())

    emit('question_comment', {'comment': comment, 'myComment': False}, broadcast=True, include_self=False)
    emit('question_comment', {'comment': comment, 'myComment': True})



    # Socket stuff

likes = {} # going to be an array/dictionary when we make it for new users

@socketio.on('connect') # when socket connects
def on_connect():
   print('Socket Connected')

   likes = run.globalLikes # assign global likes to this environment likes

   print('initial likes : ' + str(likes))

   # send over all the likes from every user
   for key in likes:
      emit('initialUpdate', {'id_name' : key, 'number': likes[key]})

@socketio.on('disconnect') # when socket dis-connects
def on_disconnect():
   print('Socket Disconnected')
   # emit('initialUpdate', {'id_name' : '<enter identifier>', 'number': likes}) probably put a emit message for disconnection as well

@socketio.on('message')
def handle_message(message):
   incoming_message = str(message)

   print('Received message : ' + incoming_message + ' Likes : ' + str(message["number"]) + ' globalLikes : ' + str(run.globalLikes)) # receiving JSON data

   # probably make this such that it works specific to the message identifier.

   run.globalLikes[message["id_name"]] = message["number"]
   likes = run.globalLikes

   emit('updateCount', message, broadcast = True) # BroadCast message to all clients