from flask import Blueprint, request, render_template, url_for, redirect
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


@chat_bp.route('/send', methods=['POST'])
def send_message():
    message = request.json
    chatMessage = ChatMessage(sender_id=1, request_id=1, message=message)
    db.session.add(chatMessage)
    db.session.commit()
    
    
    return redirect(url_for('chat.chat'))
    
