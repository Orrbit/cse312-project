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
        print("A user has joined " + str(c.id))
        emit('room_response', "Joined a room",room=c.id)


def emit_message(conversation_id, message, sender_name):
    socketio.emit('message_receive', {
        "conversation_id": conversation_id,
        "text": message.text,
        "time": message.time.isoformat(),
        "sender_id":message.sender_id,
        "name": sender_name
    }, room=int(conversation_id))
    print("I am trying to emit to " + str(conversation_id))