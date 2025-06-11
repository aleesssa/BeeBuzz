import os, re, random, string, datetime
from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify, current_app
from extensions import db, mail
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user, login_user, logout_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from models.request import Request

auth_bp = Blueprint('auth', __name__)


# ---------- Home ----------

@auth_bp.route('/')
def index():
    return render_template('index.html')


# ---------- Login ----------

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form['userInput']
        password = request.form['pwd']
        user = User.query.filter((User.username == user_input) | (User.email == user_input)).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Invalid username/email or password.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html')


# ---------- Logout ----------

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))


# ---------- Signup ----------

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

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            flash('Invalid email format.', 'danger')
            return redirect(url_for('auth.signup'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.signup'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'danger')
            return redirect(url_for('auth.signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password, phone=phone)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


# ---------- Profile ----------

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        phone = request.form.get('phone')
        nickname = request.form.get('nickname')

        current_user.phone = phone
        current_user.nickname = nickname
        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('profile.html')


# ---------- Profile Picture Upload ----------

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


# ---------- Role Toggle ----------

@auth_bp.route('/toggle_role', methods=['POST'])
@login_required
def toggle_role():
    role = request.form.get('role')
    current_user.role = 'runner' if role == 'runner' else 'shopper'
    db.session.commit()
    return redirect(url_for('auth.profile'))

#----------History Request ----------
@auth_bp.route('/history-profile', methods=['GET'])
def history():
    items_name = Request.query.filter_by(user_id=current_user.id).all()
    time = Request.query.filter_by(user_id=current_user.id).all()
    status = Request.query.filter_by(user_id=current_user.id).all()
    created_at = Request.query.filter_by(user_id=current_user.id).all()

    return render_template('profile.html', request=request)

# ---------- Password Reset ----------

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
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No account found with that email.", "danger")
        return redirect(url_for('auth.forgot_password'))

    reset_code = str(random.randint(100000, 999999))
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

    user.reset_code = reset_code
    user.reset_code_expiry = expiry_time
    db.session.commit()

    # Display code directly (easy testing/dev)
    flash(f"Your reset code is: {reset_code}", "info")

    return render_template("verify_code.html", email=email)

@auth_bp.route('/verify-code', methods=['POST'])
def verify_code():
    email = request.form.get('email')
    code = request.form.get('code')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    if user.reset_code != code:
        flash('Incorrect verification code.', 'danger')
        return render_template("verify_code.html", email=email)

    if user.reset_code_expiry < datetime.datetime.utcnow():
        flash('Verification code expired.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    return render_template("reset_password.html", email=email)

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not new_password or new_password != confirm_password:
        flash("Passwords do not match or are empty.", "danger")
        return redirect(url_for('auth.forgot_password'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.forgot_password'))

    user.password_hash = generate_password_hash(new_password)
    user.reset_code = None
    user.reset_code_expiry = None
    db.session.commit()

    flash("Password reset successfully! Please log in.", "success")
    return redirect(url_for('auth.login'))

@auth_bp.route('/home')
def home():
    return render_template('home.html')

