from extensions import db
from datetime import datetime

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time_open = db.Column(db.Time, nullable=False)
    time_close = db.Column(db.Time, nullable=False)
    is_open = db.Column(db.Boolean, nullable=False)  # e.g., Open, Closed
    last_updated = db.Column(db.DateTime, default=datetime.utcnow())