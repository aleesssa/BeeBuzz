from flask import Flask
from extensions import db, migrate

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

# Connect to SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beebuzz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'

# Initialize the database
db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()

# Register blueprints
from routes.chat_routes import chat_bp
from routes.auth_routes import auth_bp

app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)