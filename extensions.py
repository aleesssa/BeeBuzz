from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
from flask_socketio import SocketIO
=======
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
>>>>>>> auth

# Initialize db and socketio in another file to overcome circular error
db = SQLAlchemy()
<<<<<<< HEAD
socketio = SocketIO()
=======
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
>>>>>>> auth
