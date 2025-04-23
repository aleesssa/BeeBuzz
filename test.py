from models.user import User
from app import app, db

# Dummy users to test database and other functions

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
user3 = User(
    username = 'nisnis',
    email = 'nisreenathirahh@gmail.com',
    phone_number = '0132452525',
    password = '2222222',
    isRider=False,
    profile_image='img.png'
)
with app.app_context():
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    print("✅ User added:", user2.username)