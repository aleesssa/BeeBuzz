import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, request, render_template, jsonify, session, current_app
from flask_socketio import SocketIO, emit
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
    chatList = ChatMessage.query.filter_by(sender_id = user_id)
    return render_template('chat.html')

@chat_bp.route('/<int:request_id>')
def chat(request_id):
    if session.get('user_id'):
        user_id = session['user_id']
        if ((Request.query.filter_by(id = request_id).first().client_id != user_id) or Request.query.filter_by(id = request_id).first().runner_id != user_id):
            return 'Invalid request id'
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
    request_id = request.form['request_id']
    
    media_file = request.files['media']
    media_url = save_file(media_file)
    
    if sender_id == Request.query.filter_by(id = request_id).first().client_id:
        recipient_id = Request.query.filter(id = request_id).first().runner_id
    else:
        recipient_id = Request.query.filter(id = request_id).first().client_id
        
    
    chatMessage = ChatMessage(sender_id=sender_id, recipient_id=recipient_id,request_id=request_id, message=message, media_url=media_url)
    db.session.add(chatMessage)
    db.session.commit()
    
    
    return jsonify({ 
                    'sender_id': sender_id,
                    'sender_name' : sender_name,
                    'message' : message,
                    'media_url' : media_url
                    })
    
    
@socketio.on('send_message')
def broadcast_message(data):
    emit('receive_message', data, broadcast=True)
        
@socketio.on('seen_message')
def seen_message(data):
    emit('user_seen_message', data, broadcast=True)        
        
@socketio.on('is_typing_frontend')
def is_typing(data):
    emit('is_typing_backend', data, broadcast=True)        


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