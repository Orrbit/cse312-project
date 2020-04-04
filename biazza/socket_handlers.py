from biazza import socketio
from flask_socketio import emit
import lxml.html, lxml.html.clean


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