from models.user import User
from models.request import Request
from app import app, db

# Dummy users to test database and other functions

user1 = User(
    username="aleessa",
    email="aleessa@mmu.edu.my",
    phone="0123456789",
    password="hashedpassword1",
    isRider=True,
    profile_image="default.png"
)

user2 = User(
    username = 'Jaemin',
    email = 'jaemin@gmail.com',
    phone = '0104523053',
    password = '1111111',
    isRider=False,
    profile_image='image.png'
)
user3 = User(
    username = 'nisnis',
    email = 'nisreenathirahh@gmail.com',
    phone = '0132452525',
    password = '2222222',
    isRider=False,
    profile_image='img.png'
)

request = Request(
    item_name='mochi',
    pickup_location='tekun',
    dropoff_location='fci',
    price_offer=5,
    client_id=1
)

with app.app_context():
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(request)
    db.session.commit()
    print("Entries succesfully added!")