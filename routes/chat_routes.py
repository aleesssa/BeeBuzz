import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, request, render_template, jsonify, session, current_app
from extensions import db
from models.chat_message import ChatMessage
from models.user import User
from models.request import Request

chat_bp = Blueprint('chat', __name__) # Equivalent to app = Flask(__name__)


@chat_bp.route('/')
def chat():
    if session.get('user_id'):
        user_id = session['user_id']
    else:
        return 'Please log in'
    messages = ChatMessage.query.all()
    users = User.query
    # Return list of messages from database
    return render_template('chat.html', messages=messages, users=users, user_id=user_id)


# /chat_list --> shows lists of recent messages

# /<request_id> --> show message for that request

@chat_bp.route('/send', methods=['POST'])
def send_message():
    sender_id = session['user_id']
    message = request.form['message']
    
    media_file = request.files['media']
    media_url = save_file(media_file)
    
    
    chatMessage = ChatMessage(sender_id=sender_id, request_id=1, message=message, media_url=media_url)
    db.session.add(chatMessage)
    db.session.commit()
    
    
    return jsonify({ "message": "Message sent" })
    
    
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