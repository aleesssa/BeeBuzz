from flask import Blueprint, request, render_template, url_for, jsonify, session
from extensions import db
from models.chat_message import ChatMessage
from models.user import User
from models.request import Request

chat_bp = Blueprint('chat', __name__) # Equivalent to app = Flask(__name__)


@chat_bp.route('/')
def chat():
    messages = ChatMessage.query.all()
    users = User.query
    # Return list of messages from database
    return render_template('chat.html', messages=messages, users=users)


# /chat_list --> shows lists of recent messages

# /<request_id> --> show message for that request

@chat_bp.route('/send', methods=['POST'])
def send_message():
    sender_id = session['user_id']
    message = request.form['message']
    chatMessage = ChatMessage(sender_id=sender_id, request_id=1, message=message)
    db.session.add(chatMessage)
    db.session.commit()
    
    
    return jsonify({ "message": "Message sent" })
    

# Mimick login
@chat_bp.route('/simulate_login/<int:user_id>')
def simulate_login(user_id):
    session['user_id'] = user_id
    return f'Logged in as user {user_id}'