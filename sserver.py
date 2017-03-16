#!/usr/bin/env python

from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

event_name = "my_event"
namespace = "/my_namespace"

@socketio.on(event_name, namespace=namespace)
def test_message(message):
    print("called!")
    print("receive: ")
    print(message)
    #emit('aaa', message)
    send(message, namespace=namespace)

if __name__ == '__main__':
    socketio.run(app)