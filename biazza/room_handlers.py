from biazza import socketio
from flask_socketio import emit, join_room
from flask import request
from biazza.token_util import get_user_with_token
from biazza.models import Comment, Accounts, Conversation, db
from sqlalchemy import or_
import run
from datetime import datetime


waiting_conversations = {}

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
        emit('room_response', "Joined a room",room=c.id)
    
    if user.id in waiting_conversations:
        c = waiting_conversations[user.id]
        del waiting_conversations[user.id]
        print(c)
        other_id = c.user_guest_id if user.id == c.user_owner_id else c.user_owner_id
        print(other_id)
        other_account = Accounts.query.filter(Accounts.id == other_id).first()
        print(other_account)
        other_name = other_account.first_name + ' ' + other_account.last_name
        print(other_name)
        other_id = other_account.id
        emit('conversation_received', {
            "id": c.id,
            "other_id": other_id,
            "text": "Send a message now!",
            "time": datetime.now().isoformat(),
            "other_name": other_name
        },room=c.id)


def emit_message(conversation_id, message, sender_name):
    socketio.emit('message_receive', {
        "conversation_id": conversation_id,
        "text": message.text,
        "time": message.time.isoformat(),
        "sender_id":message.sender_id,
        "name": sender_name
    }, room=int(conversation_id))
    print("I am trying to emit to " + str(conversation_id))

def emit_conversation(conversation):
    socketio.emit('refresh_rooms')
    waiting_conversations[conversation.user_guest_id] = conversation
