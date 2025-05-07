from flask import Blueprint, request, render_template, url_for, redirect
from extensions import db

request_bp = Blueprint('request_bp', __name__) # Equivalent to app = Flask(__name__)

@request_bp.route('/')
def request():
   return render_template ("request.html")

@request_bp.route('/request', methods=['POST','GET'])
def handle_request():
    if request.method == 'GET':
        return render_template('request.html')
    if request.method == 'POST':
        need = request.form.get("need"),
        payment = request.form.get("payment"),
        time = request.form.get("time"),
        pickup = request.form.get("pickup"),
        dropoff = request.form.get("dropoff"),
        notes = request.form.get("notes"),
        return render_template ("summaryreq.html")
        

    