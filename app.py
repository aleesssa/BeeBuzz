<<<<<<< HEAD
from flask import Flask, session
from flask_socketio import SocketIO
from extensions import db, socketio

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

app.config['SECRET_KEY'] = 'Beebuzz'

# Connect to SQLite database
=======
import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_socketio import SocketIO

from extensions import db, migrate, socketio
from models.user import User
from routes.chat_routes import chat_bp
from routes.auth_routes import auth_bp
from routes.request_routes import request_bp

# ───────────────────────────────────────────────────────────────────────────────
# App & Config
# ───────────────────────────────────────────────────────────────────────────────
load_dotenv()

def create_app():
    app = Flask(
        __name__, 
        template_folder='templates',
        static_folder='static',
        static_url_path='/'
    )

    # Core settings
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

    return app

app = create_app()

# ───────────────────────────────────────────────────────────────────────────────
# Extensions Initialization
# ───────────────────────────────────────────────────────────────────────────────
db.init_app(app)
<<<<<<< HEAD
socketio.init_app(app)
=======
migrate.init_app(app, db)
socketio.init_app(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# ───────────────────────────────────────────────────────────────────────────────
# User Loader
# ───────────────────────────────────────────────────────────────────────────────
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ───────────────────────────────────────────────────────────────────────────────
# Blueprints Registration
# ───────────────────────────────────────────────────────────────────────────────
app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(request_bp, url_prefix='/request')

# ───────────────────────────────────────────────────────────────────────────────
# Email Utility
# ───────────────────────────────────────────────────────────────────────────────
def send_email(to_email, subject, body):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to_email])
    msg.body = body
    try:
        mail.send(msg)
        app.logger.info(f"Email sent to {to_email}")
        return True
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")
        return False

app.send_email = send_email

# ───────────────────────────────────────────────────────────────────────────────
# Command line DB init (for dev/testing)
# ───────────────────────────────────────────────────────────────────────────────
@app.before_first_request
def create_tables():
    db.create_all()

# ───────────────────────────────────────────────────────────────────────────────
# Main Route
# ───────────────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return 'Main page'

# ───────────────────────────────────────────────────────────────────────────────
# SendGrid Email Option (if you prefer SendGrid)
# ───────────────────────────────────────────────────────────────────────────────
def send_email_via_sendgrid(to_email, subject, body):
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail as SGMail, Email, To, Content

    sg_msg = SGMail(
        from_email=Email(os.getenv('SENDGRID_FROM')),
        to_emails=To(to_email),
        subject=subject,
        plain_text_content=Content("text/plain", body)
    )
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(sg_msg)
        app.logger.info(f"SendGrid status {response.status_code}")
        return True
    except Exception as e:
        app.logger.error(f"SendGrid error: {e}")
        return False

# ───────────────────────────────────────────────────────────────────────────────
# App start
# ───────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
