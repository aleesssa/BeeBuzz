import re

from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__) # Equivalent to app = Flask(__name__)

@auth_bp.route('/')
def index():
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form['userInput']
        password = request.form['pwd']

        user = User.query.filter((User.username == user_input) | (User.email == user_input)).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('chat.chat'))  # or wherever you want to go after login
        else:
            flash('Invalid username/email or password.', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        phone = request.form['phone']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('auth.signup'))
        
        if len(password) < 8 or not any(char.isdigit() for char in password):
            flash('Password must be at least 8 characters long and contain a number.', 'danger')
            return redirect(url_for('auth.signup'))
        
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            flash('Invalid email format. Please use a correct email address.', 'danger')
            return redirect(url_for('auth.signup'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered! please use a different email.', 'danger')
            return redirect(url_for('auth.signup'))
        
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username already taken! please use a different username.', 'danger')
            return redirect(url_for('auth.signup'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')