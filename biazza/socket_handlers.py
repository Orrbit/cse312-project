from biazza import socketio
from flask_socketio import emit
from biazza.models import Comment, db
import run

@socketio.on('connect') # when socket connects
def on_connect():
   print('Socket Connected')

@socketio.on('disconnect') # when socket dis-connects
def on_disconnect():
   print('Socket Disconnected')

#sent from the client whenever a like button is pressed
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

#Called after hitting the POST comment endpoint
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
      "qid": comment.question_id,
      "text": comment.text,
      "likes": comment.likes,
      "attachments": attachment_info
   }, broadcast = True)


def emit_question(question, attachments):
   attachment_info = []
   
   for attachment in attachments:
      new_attachment = {
         "path": attachment.path,
         "name": attachment.user_filename
      }
      attachment_info.append(new_attachment)
   
   socketio.emit('question_emit', {
      "id": question.id,
      "title": question.title,
   }, broadcast=True)