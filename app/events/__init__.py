from flask_socketio import send, emit
from flask_login import current_user

from .. import socketio

@socketio.on('message')
def message(data):
    send(data)

