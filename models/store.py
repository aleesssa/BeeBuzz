from extensions import db
from datetime import datetime

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # e.g., Open, Closed
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)