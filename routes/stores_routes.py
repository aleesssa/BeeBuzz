from flask import Blueprint, request, render_template, jsonify, session, current_app
from extensions import db
from models.store import Store
from datetime import datetime


stores_bp = Blueprint('stores', __name__) # Equivalent to app = Flask(__name__)


@stores_bp.route('/')
def stores():
    return render_template('stores.html')


@stores_bp.route('/add', methods = ['GET', 'POST'])
def add_store():
    if request.method == "GET":
        return render_template('store_add.html')

    if request.method == "POST":
        name = request.form.get('name')
        time_open = request.form.get('time_open')
        time_close = request.form.get('time_close')
        
        
        store = Store(
            name = name,
            time_open = time_open,
            time_close = time_close
        )
        
        db.session.add(store)
        db.session.commit()
        
        return 0
        
# Check if store is open or close
def is_open(time_open, time_close):
    now = datetime.now().time()
    return time_open <= now < time_close