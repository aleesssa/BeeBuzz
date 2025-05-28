from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

# Initialize db and socketio in another file to overcome circular error
db = SQLAlchemy()
socketio = SocketIO()
