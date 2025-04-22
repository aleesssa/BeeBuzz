from app import app, db
from models.user import User
from models.request import Request
from models.chat_message import ChatMessage
from models.rating import Rating
from models.receipt import Receipt
from models.store import Store

# Drop existing tables (optional during testing)
# db.drop_all()


# Create tables
with app.app_context():
    db.create_all()
    print("✅ Database created!")