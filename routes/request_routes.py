from flask import Blueprint, request, render_template, url_for, redirect
from extensions import db

request_bp = Blueprint('request', __name__) # Equivalent to app = Flask(__name__)

@request_bp.route('/')
def request():
    return render_template('request.html')
