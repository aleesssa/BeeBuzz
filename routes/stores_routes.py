from flask import Blueprint, request, render_template, jsonify, session, current_app, redirect, url_for
from extensions import db
from models.store import Store
from datetime import datetime, timedelta


stores_bp = Blueprint('stores', __name__) # Equivalent to app = Flask(__name__)


@stores_bp.route('/')
def stores():
    stores = Store.query.all()
    
    update_store_status(stores) # Update store status based on current time
    
    return render_template('stores.html', stores=stores, active_page='stores')


@stores_bp.route('/add', methods = ['GET', 'POST'])
def add_store():
    if request.method == "GET":
        return render_template('store_add.html', active_page='stores')

    if request.method == "POST":
        # Store's name
        name = request.form.get('name')
        
        # Convert string time to datetime object
        time_open_str = request.form.get("time_open")
        time_close_str = request.form.get("time_close")

        time_open = datetime.strptime(time_open_str, "%H:%M").time()
        time_close = datetime.strptime(time_close_str, "%H:%M").time()

        
        
        store = Store(
            name = name,
            time_open = time_open,
            time_close = time_close,
            is_open = is_open(time_open, time_close)
        )
        
        db.session.add(store)
        db.session.commit()
        
        return redirect(url_for('stores.stores'))
        
        
# Check if store is open or close
def is_open(time_open, time_close):
    now = datetime.utcnow() + timedelta(hours=8)
    # now = time(23, 30)
    return time_open <= now < time_close

# Update store status
def update_store_status(stores):
    for store in stores:
        time_open = store.time_open    
        time_close = store.time_close
        store_status = is_open(time_open, time_close)
        
        if store.is_open != store_status:
            store.is_open = store_status
        
    db.session.commit()