import os
from flask import Flask
from flask_mail import Mail
from extensions import db, migrate, login_manager
from models.user import User
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beebuzz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key_here')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

db.init_app(app)
migrate.init_app(app, db)
mail = Mail(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from routes.chat_routes import chat_bp
from routes.auth_routes import auth_bp

app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

