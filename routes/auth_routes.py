import re, os, random, datetime
from flask import Blueprint, request, render_template, redirect, url_for, flash, session, current_app
from extensions import db, mail
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user, login_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from utils.email_utils import send_email  

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
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('auth.profile'))  # or wherever you want to go after login
        else:
            flash('Invalid username/email or password.', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('login.html')

from flask_login import logout_user

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))


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

#==== Password Reset ====#

from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.secret_key)
    return serializer.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.secret_key)
    try:
        return serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except:
        return None

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('forgot_password.html')

@auth_bp.route('/send-reset-code', methods=['POST'])
def send_reset_code():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Email not found', 'error')
        return redirect(url_for('auth.forgot_password'))

    code = str(random.randint(100000, 999999))
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

    user.reset_code = code
    user.reset_code_expiry = expiry
    db.session.commit()

    send_email(
        to_email=user.email,
        subject="Reset Code",
        body="Here is your code..."
    )

    flash('Verification code sent to your email', 'info')
    return render_template('verify_code.html', email=email)


# Step 3: Verify code page
@auth_bp.route('/verify-code', methods=['POST'])
def verify_code():
    email = request.form['email']
    code = request.form['code']
    user = User.query.filter_by(email=email).first()

    if not user or user.reset_code != code or user.reset_code_expiry < datetime.datetime.utcnow():
        flash('Invalid or expired code', 'error')
        return redirect(url_for('auth.forgot_password'))

    return render_template('reset_password.html', email=email)

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.form['email']
    password = request.form['password']
    confirm = request.form['confirm']

    if password != confirm:
        flash('Passwords do not match', 'error')
        return redirect(url_for('auth.forgot_password'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('auth.forgot_password'))

    user.password_hash = generate_password_hash(password)
    user.reset_code = None
    user.reset_code_expiry = None
    db.session.commit()

    flash('Password successfully reset. You may now log in.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Handle profile update
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')

        # Update the current user information
        current_user.username = username
        current_user.email = email
        current_user.phone = phone

        # Commit changes to the database
        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))

    # Handle the GET request: display the profile page
    return render_template('profile.html')


UPLOAD_FOLDER = 'static/profile_pics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@auth_bp.route('/upload-profile-pic', methods=['POST'])
@login_required
def upload_profile_pic():
    file = request.files.get('profile_pic')
    if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        current_user.profile_pic = filename
        db.session.commit()
        flash('Profile picture updated!', 'success')
    else:
        flash('Invalid file type.', 'danger')
    return redirect(url_for('auth.profile'))

@auth_bp.route('/toggle_role', methods=['POST'])
@login_required
def toggle_role():
    if request.form.get('role') == 'runner':
        current_user.role = 'runner'
    else:
        current_user.role = 'shopper'
    db.session.commit()
    return redirect(url_for('auth.profile'))
