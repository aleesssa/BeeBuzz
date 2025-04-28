from app import app
from extensions import db
from models.user import User  # or from models.user import User if it's inside models folder

with app.app_context():
    db.session.query(User).delete()
    db.session.commit()
    print("All users deleted successfully!")

