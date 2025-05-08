from flask import Blueprint, request, render_template, url_for, redirect
from extensions import db
from models.request import Request

request_bp = Blueprint('request_bp', __name__) # Equivalent to app = Flask(__name__)

@request_bp.route('/')
def request_job():
   return render_template ("request.html")

@request_bp.route('/request', methods=['GET','POST'])
def handle_request():
    if request.method == 'POST':
        new_request = Request(
            item_name=request.form.get("need"),
            price_offer=request.form.get("payment"),
            Time=request.form.get("time"),
            pickup_location=request.form.get("pickup"),
            dropoff_location=request.form.get("dropoff"),
            notes=request.form.get("notes")
        )
        db.session.add(new_request)
        db.session.commit()

        return render_template("summaryreq.html", data=request.form)
    return render_template("request.html")
        

    