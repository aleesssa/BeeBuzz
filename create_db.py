from flask import Flask
from extensions import db
from models.user import User
from models.request import Request
from models.chat_message import ChatMessage
from models.rating import Rating
from models.receipt import Receipt
from models.store import Store

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beebuzz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database created!")
