from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

# Connect to SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beebuzz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
