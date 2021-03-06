from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit, join_room, rooms
from threading import Lock
import os
import eventlet

SIGNALLING_NAMESPACE = '/signalling'
TEST_NAMESPACE = '/test'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PLACEHOLDER'

socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/testclient')
def test_client():
    return render_template('testclient.html')

@socketio.on('disconnect', namespace=SIGNALLING_NAMESPACE)
def test_disconnect():
    print('Client disconnected')

@socketio.on('connect', namespace=SIGNALLING_NAMESPACE)
def connected():
    print('Connected')
    emit('response',{'message': 'Connection Successful!!'})

@socketio.on('get_response', namespace=SIGNALLING_NAMESPACE)
def test_response(message):
    print(message['data'])
    emit('response',{'message': message['data']})

@socketio.on('register_endpoint_server', namespace=SIGNALLING_NAMESPACE)
def register_user(message):
    print(message['id'])
    print(message['type'])
    room = message['id']
    join_room(room)
    emit('response',{'message':'In rooms: {}'.format(room)})

@socketio.on('send_sdp_message', namespace=SIGNALLING_NAMESPACE)
def get_endpoint_server(message):
    print(message['endpoint_server_id'])
    room = message['endpoint_server_id']
    sdp_message = message['sdp_message']
    emit('sdp_message', {'sdp_message':sdp_message}, room=room)

@socketio.on('send_ice_candidate', namespace=SIGNALLING_NAMESPACE)
def get_endpoint_server(message):
    print(message['endpoint_server_id'])
    room = message['endpoint_server_id']
    ice_candidates = message['ice_candidates']
    emit('ice_candidate_message', {'ice_candidates':ice_candidates}, room=room)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 33507))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)