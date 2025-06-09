from extensions import db
from datetime import datetime

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    pickup_location = db.Column(db.String(100), nullable=False)
    dropoff_location = db.Column(db.String(100), nullable=False)
<<<<<<< HEAD
    price_offer = db.Column(db.Float, nullable=False)
=======
    price_offer = db.Column(db.String(20), nullable=False)
>>>>>>> auth
    time = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='requested')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    runner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)