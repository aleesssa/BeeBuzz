<<<<<<< HEAD
from flask import Flask, session
from flask_socketio import SocketIO
from extensions import db, socketio

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

app.config['SECRET_KEY'] = 'Beebuzz'

# Connect to SQLite database
=======
import os
from flask import Flask, request, jsonify, session
from flask_login import LoginManager, login_required, current_user  
from flask_mail import Mail, Message
from extensions import db, migrate, login_manager
from models.user import User
from dotenv import load_dotenv
from routes import request_routes
from routes.request_routes import request_bp

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')


>>>>>>> auth
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beebuzz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key_here')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_generated_app_password_here'


db.init_app(app)
<<<<<<< HEAD
socketio.init_app(app)
=======
migrate.init_app(app, db)

mail = Mail(app)

def send_email(to_email, subject, body):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to_email])
    msg.body = body
    try:
        mail.send(msg)
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    
app.send_email = send_email

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
>>>>>>> auth

from routes.chat_routes import chat_bp
<<<<<<< HEAD
from routes.request_routes import request_bp

app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(request_bp, url_prefix='/request')

@app.route('/')
def index():
    return 'Main page'

if __name__ == '__main__':
    socketio.run(app, debug=True)
=======
from routes.auth_routes import auth_bp

app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(request_bp, url_prefix='/request')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail as SGMail, Email, To, Content

def send_email_sendgrid(to_email, subject, body):
    from_email = Email("your_verified_sendgrid_email@domain.com")
    to_email_obj = To(to_email)
    content = Content("text/plain", body)
    mail = SGMail(from_email, to_email_obj, subject, content)
    sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY', 'your_sendgrid_api_key_here'))
    try:
        response = sg.send(mail)
        print(response.status_code)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    
#@app.before_request
#def auto_login_from_db():
#    if 'user_id' not in session:
#        default_user = User.query.first()  # You can also use filter_by(email='test@example.com').first()
#        if default_user:
#            session['user_id'] = default_user.id
>>>>>>> auth
