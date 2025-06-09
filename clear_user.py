from flask import Flask
from extensions import db
from models.user import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beebuzz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.session.query(User).delete()
    db.session.commit()
    print("All users deleted successfully!")
