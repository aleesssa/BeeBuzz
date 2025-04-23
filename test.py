from models.user import User
from app import app, db

user1 = User(
    username="aleessa",
    email="aleessa@mmu.edu.my",
    phone_number="0123456789",
    password="hashedpassword1",
    isRider=True,
    profile_image="default.png"
)

user2 = User(
    username = 'Jaemin',
    email = 'jaemin@gmail.com',
    phone_number = '0104523053',
    password = '1111111',
    isRider=False,
    profile_image='image.png'
)

with app.app_context():
    db.session.add(user2)
    db.session.commit()
    print("✅ User added:", user2.username)