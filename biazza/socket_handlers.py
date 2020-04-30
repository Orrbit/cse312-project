from biazza import socketio
from flask_socketio import emit
from flask import request
from biazza.token_util import get_user_with_token
from biazza.models import Comment, Accounts, db
import run

# socket id -> user
active_sockets = {}


@socketio.on('connect')  # when socket connects
def on_connect():
    token = request.cookies.get('biazza_token')
    user = get_user_with_token(token)

    if not user:
        return False
    active_sockets[request.sid] = user


@socketio.on('disconnect')  # when socket dis-connects
def on_disconnect():
    active_sockets.pop(request.sid, None)
    print('Socket Disconnected')


# sent from the client whenever a like button is pressed
@socketio.on('like_click')
def handle_message(data):
    incoming_data = str(data)

    print('Received message : ' + incoming_data + ' Is Like : ' + str(data["is_like"]))  # receiving JSON data

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

    emit('like_status', like_obj, broadcast=True)  # BroadCast message to all clients


# Called after hitting the POST comment endpoint
def emit_comment(comment, attachments):
    attachment_info = []
    for attachment in attachments:
        new_attachment = {
            "path": attachment.path,
            "name": attachment.user_filename
        }
        attachment_info.append(new_attachment)

    poster = Accounts.query.filter(Accounts.id == comment.user_id).first()

    socketio.emit('comment_emit', {
        "id": comment.id,
        "qid": comment.question_id,
        "text": comment.text,
        "likes": comment.likes,
        "attachments": attachment_info,
        "name": poster.first_name + ' ' + poster.last_name
    }, broadcast=True)


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
