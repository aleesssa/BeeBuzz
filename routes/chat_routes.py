import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, request, render_template, jsonify, session, current_app
from flask_socketio import SocketIO, emit, join_room
from extensions import db, socketio
from models.chat_message import ChatMessage
from models.user import User
from models.request import Request

chat_bp = Blueprint('chat', __name__) # Equivalent to app = Flask(__name__)

# Show list of recent chats
@chat_bp.route('/')
def chatList():
    if session.get('user_id'):
        user_id = session['user_id']
        
    request_ids = [
    r[0] for r in db.session.query(ChatMessage.request_id)
    .filter(
        (ChatMessage.sender_id == user_id) |
        (ChatMessage.recipient_id == user_id)
    )
    .distinct()
    .all()
]
    
    return render_template('chatList.html', request_ids = request_ids)

@chat_bp.route('/<int:request_id>')
def chat(request_id):
    client_id = Request.query.filter_by(id = request_id).first().client_id
    runner_id = Request.query.filter_by(id = request_id).first().runner_id
    if session.get('user_id'):
        user_id = session['user_id']
        if (user_id != client_id and user_id != runner_id):
            return f'Invalid request id\nUserID = {user_id} \n ClientID : {client_id}\nRunnerID : {runner_id}'
    else:
        return 'Please log in'
    
    messages = ChatMessage.query.filter_by(request_id=request_id)
    users = User.query
    # Return list of messages from database
    return render_template('chat.html', messages=messages, users=users, user_id=user_id, request_id=request_id)

@chat_bp.route('/send', methods=['POST'])
def send_message():
    sender_id = session['user_id']
    sender_name = User.query.filter_by(id=sender_id).first().username
    message = request.form['message']
    request_id = int(request.form['request_id'])
    
    media_file = request.files['media']
    media_url = save_file(media_file)
    
    req = Request.query.get(request_id)
    if not req:
        return "Invalid request", 400

    # Check if sender is part of the request
    if sender_id not in [req.client_id, req.runner_id]:
        return "Unauthorized", 403

    recipient_id = req.runner_id if sender_id == req.client_id else req.client_id
        
    chatMessage = ChatMessage(sender_id=sender_id, recipient_id=recipient_id, request_id=request_id, message=message, media_url=media_url)
    db.session.add(chatMessage)
    db.session.commit()
    
    
    return jsonify({ 
                    'sender_id': sender_id,
                    'sender_name' : sender_name,
                    'request_id': request_id,
                    'message' : message,
                    'media_url' : media_url
                    })
    
    
@socketio.on('join_room')    
def handle_join_room(data):
    room = data['request_id']
    join_room(room)
    print(f'User joined room {room}')
    
@socketio.on('send_message')
def broadcast_message(data):
    emit('receive_message', data, room=data['request_id'])
        
@socketio.on('seen_message')
def seen_message(data):
    user_id = data['user_id']
    request_id = data['request_id']
    
    # Update database
    ChatMessage.query.filter_by(
        recipient_id = user_id,
        request_id = request_id,
        is_seen = False
    ).update({'is_seen' : True})
    
    db.session.commit()
    
    emit('user_seen_message', data, room=request_id)        
        
@socketio.on('is_typing_frontend')
def is_typing(data):
    emit('is_typing_backend', data, room=data['request_id'])        


def save_file(media_file):
    # Check if media_file exists
    if not media_file:
        return None
    
    # Save file and return media_url
    ext = os.path.splitext(media_file.filename)[1] # Get file extension
    filename = secure_filename(f'{uuid.uuid4()}{ext}') # Create filename
    
    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads') 
    os.makedirs(upload_dir, exist_ok=True) # Create upload dir if it does not exist
    
    file_path = os.path.join(upload_dir, filename)
    media_file.save(file_path)
    
    return f'/uploads/{filename}'

# Mimick login
@chat_bp.route('/simulate_login/<int:user_id>')
def simulate_login(user_id):
    session['user_id'] = user_id
    return f'Logged in as user {user_id}'