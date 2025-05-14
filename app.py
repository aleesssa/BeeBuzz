import os
import sendgrid
from sendgrid.helpers.mail import Mail,Email,To,Content
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from extensions import db, migrate, login_manager
from models.user import User
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

SENDGRID_API_KEY = 'your_sendgrid_api_key'
sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beebuzz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key_here')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'

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

def send_email(to_email, subject, body):
    from_email = Email("your_verified_sendgrid_email@domain.com")
    to_email = To(to_email)
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content)
    
    try:
        response = sg.send(mail)
        print(response.status_code)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False