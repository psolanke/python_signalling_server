from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit, join_room
# from storage_utils import StorageManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PLACEHOLDER'

socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/testclient')
def test_client():
	return render_template('testclient.html')

@socketio.on('connect', namespace='/signalling')
def connected():
	print('Connected')
	emit('response',{'message': 'Thank you for connecting'})

@socketio.on('get_response', namespace='/signalling')
def test_response(message):
	print(message['data'])
	emit('response',{'message': message['data']})

@socketio.on('register_endpoint_server', namespace='/signalling')
def register_user(message):
	print(message['id'])
	print(message['type'])
	room = message['id']
	join_room(room)

@socketio.on('contact_endpoint_server', namespace='/signalling')
def get_endpoint_server(message):
	print(message['endpoint_server_id'])
	room = message['endpoint_server_id']
	sdp_message = message['sdp_message']
	emit('sdp_message', {'sdp_message':sdp_message}, room=room)


if __name__ == '__main__':
	socketio.run(app, debug=True)