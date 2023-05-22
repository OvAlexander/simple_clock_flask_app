#Project Description
#Simple Flask webapp that updates and displays the current time
#python -m venv env : makes a virtual enviroment
#.\env\Scripts\activate : nav to virtual enviroment and activate it
#https://docs.python.org/3/library/time.html
#https://www.geeksforgeeks.org/python-time-localtime-method/#
#https://stackoverflow.com/questions/4271740/how-can-i-use-python-to-get-the-system-hostname
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import socket
#defines a rout and view funcation


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you_secret_key'
socketio = SocketIO(app)


@app.route('/')
def home():
    name = socket.gethostname()
    get_time = time.localtime()
    time_str = time.asctime(get_time)
    return render_template('index.html',name = name, time = time_str)

@socketio.on('connect')
def handle_connect():
    print('Client Connected')
    send_updates()

@socketio.on('disconnect')
def handle_disconnect():
    print('Client Disconnected')

@socketio.on('request_updates')
def handle_request_updates():
    send_updates()

# @socketio.on('message')
# def handle_message(data):
#     print('Data recieved', data)
#     emit('update', {'message': 'Data updated'})
@socketio.on('update')
def handle_updates():
    send_updates()

def send_updates():
    get_time = time.localtime()
    time_str = time.asctime(get_time)
    data = {
        'time': time_str
    }
    print('Data recieved', data)
    emit('update', data, brodcast=True)

if __name__ == '__main__':
    #app.run()
    socketio.run(app)