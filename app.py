import eventlet
eventlet.monkey_patch()

import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_socketio import SocketIO

from extensions import db, migrate, socketio
from models.user import User
from models.store import Store
from routes.chat_routes import chat_bp
from routes.stores_routes import stores_bp
from routes.auth_routes import auth_bp
from routes.request_routes import request_bp

from datetime import time

load_dotenv()

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static',
        static_url_path='/'
    )
    app.config.update({
        'SECRET_KEY': os.getenv('SECRET_KEY', 'super-secret-key'),
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///beebuzz.db',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'MAIL_SERVER': 'smtp.gmail.com',
        'MAIL_PORT': 587,
        'MAIL_USE_TLS': True,
        'MAIL_USERNAME': os.getenv('MAIL_USERNAME'),
        'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD'),
    })

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)
    mail = Mail(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(stores_bp, url_prefix='/stores')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(request_bp, url_prefix='/request')

    # Current Request
    @app.context_processor
    def inject_current_request():
        from flask_login import current_user
        from flask import url_for
        from models.request import Request

        order_link = url_for('request_bp.request_job')
        current_request = None

        if current_user.is_authenticated:
            current_request = Request.query.filter_by(client_id=current_user.id)\
                .filter(Request.status != 'completed')\
                .order_by(Request.created_at.desc())\
                .first()
            
            if current_request:
                order_link = url_for('request_bp.track_status', request_id=current_request.id)

        return dict(current_request=current_request, order_link=order_link)


    # Add system as a user in database
    def add_system():
        # Check if system user already exists 
        existing_system = User.query.filter_by(email="system@beebuzz.app").first()

        if not existing_system:
            system_user = User(
                username="BeeBuzz System",
                email="system@beebuzz.app",
                password_hash="system",  # won't ever log in
                role=False
            )
            db.session.add(system_user)
            db.session.commit()
            print("System user created.")
        else:
            print("System user already exists.")


    # Store seeding
    def seed_store():
        if Store.query.count() == 0:
            stores = [
                Store(
                    name='7E',
                    is_open=0,
                    open_time=time(0, 0),
                    close_time=time(23, 59)
                ),
                Store(
                    name='Haji Tapah',
                    is_open=0,
                    open_time=time(9, 0),
                    close_time=time(17, 00)
                ),
                Store(
                    name='BookShop',
                    is_open=0,
                    open_time=time(8, 0),
                    close_time=time(19, 00)
                ),
                Store(
                    name='Dapo Sahang',
                    is_open=0,
                    open_time=time(11, 0),
                    close_time=time(23, 00)
                ),
                Store(
                    name='Deen',
                    is_open=0,
                    open_time=time(11, 0),
                    close_time=time(23, 00)
                ),
                Store(
                    name='Bakery',
                    is_open=0,
                    open_time=time(11, 0),
                    close_time=time(23, 00)
                ),
                Store(
                    name='FOM Cafe',
                    is_open=0,
                    open_time=time(11, 0),
                    close_time=time(23, 00)
                )
            ]
            db.session.bulk_save_objects(stores)
            db.session.commit()
                
    # One-time startup logic
    with app.app_context():
        db.create_all()
        add_system()
        seed_store()

    return app

app = create_app()


@app.route('/')
def index():
    return render_template('index.html')

        

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)

