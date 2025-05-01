from flask import Blueprint, request, render_template, url_for, redirect
from extensions import db

request_bp = Blueprint('request', __name__) # Equivalent to app = Flask(__name__)

@request_bp.route('/', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'GET':
      return render_template("index.html")
    elif request.method == 'POST':
      form_data = {
        "need": request.form.get("need"),
        "payment": request.form.get("payment"),
        "time":  request.form.get("time"),
        "pickup": request.form.get("pickup"),
        "dropoff": request.form.get("dropoff"),
        "notes": request.form.get("notes"),
      }

      return render_template("summaryreq.html", data=form_data)