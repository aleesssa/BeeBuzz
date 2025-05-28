from flask import Flask, session
from flask_socketio import SocketIO
from extensions import db, socketio

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

app.config['SECRET_KEY'] = 'Beebuzz'

# Connect to SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beebuzz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
socketio.init_app(app)

# Register blueprints
from routes.chat_routes import chat_bp
from routes.request_routes import request_bp

app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(request_bp, url_prefix='/request')

@app.route('/')
def index():
    return 'Main page'

if __name__ == '__main__':
    socketio.run(app, debug=True)