from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_socketio import SocketIO

# Initialize db and socketio in another file to overcome circular error
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()
mail = Mail()
login_manager = LoginManager()
