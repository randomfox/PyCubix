# https://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abutttuba'
socketio = SocketIO(app)

# @app.route('/')
# def index():
#     return render_template('index.html')

@socketio.on('test', namespace='/test')
def test_message(message):
    emit('server says', {'data': message['data']})

# @socketio.on('my broadcast event', namespace='/test')
# def test_message(message):
#     emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('server says', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
