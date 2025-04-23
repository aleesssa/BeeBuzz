from app import db

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    runner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    approved = db.Column(db.Boolean, default=False)