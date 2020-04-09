from biazza import socketio
from flask_socketio import emit
from biazza.models import Comment, db
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

@socketio.on('connect') # when socket connects
def on_connect():
   print('Socket Connected')

   likes = run.globalLikes # assign global likes to this environment likes

   # send over all the likes from every user
   for key in likes:
      emit('initialUpdate', {'comment_id' :  key, 'number': likes[key]})

@socketio.on('disconnect') # when socket dis-connects
def on_disconnect():
   print('Socket Disconnected')
   # emit('initialUpdate', {'id_name' : '<enter identifier>', 'number': likes}) probably put a emit message for disconnection as well

@socketio.on('like_click')
def handle_message(data):
   incoming_data = str(data)

   print('Received message : ' + incoming_data + ' Is Like : ' + str(data["is_like"])) # receiving JSON data

   comment = Comment.query.get(data["comment_id"])
   if data["is_like"]:
      comment.likes = comment.likes + 1
   else:
      comment.likes = comment.likes - 1
   db.session.commit()

   like_obj = {
      "comment_id": data["comment_id"],
      "likes": comment.likes
   }

   emit('like_status', like_obj, broadcast = True) # BroadCast message to all clients

def emit_comment(comment, attachments):
   attachment_info = []
   for attachment in attachments:
      new_attachment = {
         "path": attachment.path,
         "name": attachment.user_filename
      }
      attachment_info.append(new_attachment)
   socketio.emit('comment_emit', {
      "id": comment.id,
      "text": comment.text,
      "likes": comment.likes,
      "attachments": attachment_info
   }, broadcast = True)