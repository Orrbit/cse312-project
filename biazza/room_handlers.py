from biazza import socketio
from flask_socketio import emit, join_room
from flask import request
from biazza.token_util import get_user_with_token
from biazza.models import Comment, Accounts, Conversation, db
from sqlalchemy import or_
import run

@socketio.on('enter_rooms')  # when socket connects
def enter_rooms():
    token = request.cookies.get('biazza_token')
    user = get_user_with_token(token)

    if not user:
        return False
    

    my_conversations = Conversation.query.filter(or_(Conversation.user_owner_id == user.id,
                                                        Conversation.user_guest_id == user.id))
    rooms_joined = 0
    for c in my_conversations:
        join_room(c.id)
        rooms_joined = rooms_joined + 1

    emit('room_response', {"rooms_joined": rooms_joined})