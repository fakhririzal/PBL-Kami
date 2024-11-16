from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Dictionary untuk menyimpan room dan user
rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('create_room')
def handle_create_room(data):
    user_name = data['userName']
    room_code = data['roomCode']

    # Buat room baru jika belum ada
    if room_code not in rooms:
        rooms[room_code] = {'users': []}

    # Tambahkan user ke room
    rooms[room_code]['users'].append(user_name)
    join_room(room_code)

    print(f"Room {room_code} created by {user_name}")
    socketio.emit('create_room', {'userName': user_name, 'roomCode': room_code}, room=request.sid)

@socketio.on('join_room')
def handle_join_room(data):
    user_name = data['userName']
    room_code = data['roomCode']

    if room_code in rooms:
        # Tambahkan user ke room jika room ada
        rooms[room_code]['users'].append(user_name)
        join_room(room_code)
        print(f"{user_name} joined room {room_code}")
        socketio.emit('join_room', {'userName': user_name, 'roomCode': room_code}, room=room_code)
    else:
        # Kirim error jika room tidak ada
        socketio.emit('error', {'message': 'Invalid Room Code.'}, room=request.sid)

@socketio.on('message')
def handle_message(data):
    message = data['message']
    user_name = data['userName']
    room_code = data['roomCode']
    socket_id = data['socket_id']

    print(f"Message in room {room_code} from {user_name}: {message}")  # Pesan yang tercetak akan berupa pesan terenkripsi
    time = datetime.now().strftime('%H:%M')  # Format jam dan menit
    socketio.emit('message', {
    'message': message,
    'userName': user_name,
    'socket_id': socket_id,
    'time': time  # Tambahkan waktu
    }, room=room_code)

@socketio.on('leave_room')
def handle_leave_room(data):
    user_name = data['userName']
    room_code = data['roomCode']

    if room_code in rooms:
        # Hapus user dari room
        rooms[room_code]['users'].remove(user_name)
        leave_room(room_code)
        print(f"{user_name} left room {room_code}")

        # Hapus room jika kosong
        if not rooms[room_code]['users']:
            del rooms[room_code]

    socketio.emit('leave_room', {'userName': user_name, 'roomCode': room_code}, room=room_code)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5555, debug=True)
