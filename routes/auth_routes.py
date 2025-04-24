from flask import Blueprint, request, render_template
from extensions import db

auth_bp = Blueprint('auth', __name__) # Equivalent to app = Flask(__name__)

@auth_bp.route('/')
def index():
    return render_template('index.html')

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/signup')
def signup():
    return render_template('signup.html')