from flask import Blueprint, request, render_template, url_for, redirect, session
from extensions import db
from models.request import Request
from datetime import datetime

request_bp = Blueprint('request_bp', __name__) # Equivalent to app = Flask(__name__)

@request_bp.route('/')
def request_job():
     return render_template ("request.html")

@request_bp.route('/req', methods=['GET','POST'])
def handle_request():
    if request.method == 'POST':
        if "cancel" in request.form:
         cancelled_request = Request(
            item_name=request.form.get("need"),
            price_offer=request.form.get("payment"),
            time=request.form.get("time"),
            pickup_location=request.form.get("pickup"),
            dropoff_location=request.form.get("dropoff"),
            notes=request.form.get("notes"),
            created_at=datetime.utcnow(),
            client_id=session.get('user_id'),
            status= 'cancelled'
              )
        
        db.session.add(cancelled_request)
        db.session.commit()

        new_request = Request(
            item_name=request.form.get("need"),
            price_offer=request.form.get("payment"),
            time=request.form.get("time"),
            pickup_location=request.form.get("pickup"),
            dropoff_location=request.form.get("dropoff"),
            notes=request.form.get("notes"),
            created_at=datetime.utcnow(),
            client_id=session.get('user_id'),
            status='requested'
              )
        
        db.session.add(new_request)
        db.session.commit()

        return render_template("summaryreq.html", data=request.form)
    return render_template("request.html")
        
@request_bp.route('/login/<user_id>')
def log_in(user_id):
    session['user_id'] = user_id
    return f'Logged in as {user_id}'