from flask import Flask, render_template
from extensions import db

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

# Connect to SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beebuzz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Register blueprints
from routes.chat_routes import chat_bp
from routes.request_routes import request_bp

app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(request_bp, url_prefix='/request')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

