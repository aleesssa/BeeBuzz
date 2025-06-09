from extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
<<<<<<< HEAD
    nickname = db.Column(db.String(150), unique=True, nullable=True)
=======
    nickname = db.Column(db.String(150), nullable=True)
>>>>>>> auth
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    profile_pic = db.Column(db.String(120), nullable=False, default='default.jpg')
    role = db.Column(db.String(20), default='shopper')
    reset_code = db.Column(db.String(6), nullable=True)
<<<<<<< HEAD
    reset_code_expiry = db.Column(db.DateTime, nullable=True)
=======
    reset_code_expiry = db.Column(db.DateTime, nullable=True)
    
>>>>>>> auth
