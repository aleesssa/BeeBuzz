from extensions import db
from models.user import User
from models.request import Request

class Rating(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    request = db.relationship('Request', back_populates='ratings')
    user = db.relationship('User', back_populates='ratings')


User.ratings = db.relationship('Rating', back_populates='user')
