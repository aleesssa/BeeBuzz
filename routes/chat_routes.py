from flask import Blueprint, request, render_template
from extensions import db
from models.chat_message import ChatMessage

chat_bp = Blueprint('chat', __name__) # Equivalent to app = Flask(__name__)

@chat_bp.route('/')
def chat():
    return render_template('chat.html')


@chat_bp.route('/chat/send', methods=['POST'])
def send_message():
    return ""
    
