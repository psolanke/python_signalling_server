from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit

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

if __name__ == '__main__':
	socketio.run(app, debug=True)