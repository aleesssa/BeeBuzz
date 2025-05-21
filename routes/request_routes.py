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
    return render_template("summaryreq.html", data=new_request, request_id=new_request.id)

@request_bp.route('/edit/<int:request_id>')
def edit_request(request_id):
    req = Request.query.get_or_404(request_id)
    return render_template("update.html",request=req)

@request_bp.route('/update/<int:request_id>', methods=['POST'])
def update_request(request_id):
    req = Request.query.get_or_404(request_id)
    
    if req.client_id != session.get('user_id'):
      return "Unauthorized", 403 

    if request.form.get('_method') == 'PUT':
       item_name = request.form.get("need")
       if item_name: req.item_name = item_name
       price_offer = request.form.get("payment")
       if price_offer: req.price_offer = price_offer
       time = request.form.get("time")
       if time: req.time = time
       pickup = request.form.get("pickup")
       if pickup: req.pickup_location = pickup
       dropoff = request.form.get("dropoff")
       if dropoff: req.dropoff_location = dropoff
       notes = request.form.get("notes")
       if notes: req.notes = notes

       req.updated_at = datetime.utcnow()
        
    
    db.session.commit()
    return redirect(url_for('request_bp.summary_request', request_id=req.id))

@request_bp.route('/summary/<int:request_id>')
def summary_request(request_id):
    req = Request.query.get_or_404(request_id)
    return render_template("summaryreq.html", data=req, request_id=req.id)

@request_bp.route('/cancelled/<int:request_id>', methods=['POST'])
def cancel_request(request_id):
    req = Request.query.get_or_404(request_id)
    if req.client_id != session.get('user_id'):
        return "Unauthorized", 403

    req.status = "cancelled"
    req.updated_at = datetime.utcnow()
    db.session.commit()

    return "Your order has been cancelled."

@request_bp.route('/jobs')
def show_jobs():
    jobs = Request.query.filter_by(status="requested").all()
    return render_template("job.html", jobs=jobs)

@request_bp.route('/jobs/details/<int:request_id>')
def view_details(request_id):
    req = Request.query.get_or_404(request_id)
    return render_template("request_details.html", job_request=req)

@request_bp.route('/jobs/accept/<int:request_id>', methods=['POST'])
def accept_jobs(request_id):
    req = Request.query.get_or_404(request_id)

    if req.status == "requested":
       req.status = "accepted"
       req.runner_id = session.get('user_id')
    db.session.commit()
    
    return render_template("job.html")

@request_bp.route('/login/<int:user_id>')
def log_in(user_id):
    session['user_id'] = user_id
    return f'Logged in as {user_id}'
