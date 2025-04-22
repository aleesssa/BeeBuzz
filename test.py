from models.user import User
from app import app, db

user = User(
    username="aleessa",
    email="aleessa@mmu.edu.my",
    phone_number="0123456789",
    password="hashedpassword1",
    isRider=True,
    profile_image="default.png"
)

with app.app_context():
    db.session.add(user)
    db.session.commit()
    print("✅ User added:", user.username)