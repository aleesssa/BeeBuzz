import smtplib
from flask import Flask
from extensions import db, migrate, mail, login_manager
from models.user import User
from dotenv import load_dotenv
import os


load_dotenv()

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

# Connect to SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beebuzz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

# Initialize the database
db.init_app(app)
migrate.init_app(app, db)
mail.init_app(app)


with app.app_context():
    db.create_all()

login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Register blueprints
from routes.chat_routes import chat_bp
from routes.auth_routes import auth_bp

app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)