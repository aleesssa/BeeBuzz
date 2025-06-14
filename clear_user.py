from flask import Flask
from extensions import db, migrate, socketio, mail
from models.user import User

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beebuzz.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.session.query(User).delete()
        db.session.commit()
        print("All users deleted successfully!")

    db.create_all()

    return app
app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)