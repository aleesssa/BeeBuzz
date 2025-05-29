from flask import Blueprint, request, render_template, jsonify, session, current_app
from extensions import db
from models.chat_message import ChatMessage
from models.user import User
from models.request import Request
from models.store import Store


stores_bp = Blueprint('stores', __name__) # Equivalent to app = Flask(__name__)


@stores_bp.route('/')
def stores():
    return render_template('stores.html')

@stores_bp.route('/add', methods = ['GET', 'POST'])
def add_store():
    if request.method == "GET":
        return render_template('store_add.html')

    if request.method == "POST":
        return 0
        