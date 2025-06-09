from flask import Blueprint, request, render_template, url_for, redirect, session
<<<<<<< HEAD
from extensions import db
from models.request import Request
from datetime import datetime
=======
from flask_login import current_user, login_required
from extensions import db
from models.request import Request
from datetime import datetime
from models.user import User
>>>>>>> auth

request_bp = Blueprint('request_bp', __name__) # Equivalent to app = Flask(__name__)

@request_bp.route('/')
def request_job():
     return render_template ("request.html")

@request_bp.route('/req', methods=['GET','POST'])
<<<<<<< HEAD
def handle_request():
    price_offer = float(request.form.get("payment"))

    if request.method == 'POST':
       new_request = Request(
            item_name=request.form.get("need"),
            price_offer=price_offer,
=======
@login_required
def handle_request():
    if request.method == 'POST':
        client_id = current_user.id
        item_name = request.form.get('item_name')
        pickup_location = request.form.get('pickup_location')
        dropoff_location = request.form.get('dropoff_location')
        price_offer = request.form.get('price_offer')
        time = request.form.get('time')
        notes = request.form.get('notes')

        new_request = Request(
            item_name=request.form.get("need"),
            price_offer=request.form.get("payment"),
>>>>>>> auth
            time=request.form.get("time"),
            pickup_location=request.form.get("pickup"),
            dropoff_location=request.form.get("dropoff"),
            notes=request.form.get("notes"),
            created_at=datetime.utcnow(),
<<<<<<< HEAD
            client_id=session.get('user_id'),
            status='requested'
              )
        
       db.session.add(new_request)
       db.session.commit()
    return render_template("summaryreq.html", data=new_request, request_id=new_request.id)
=======
            client_id=current_user.id,
            runner_id=None,
            status='requested'
        )
        db.session.add(new_request)
        db.session.commit()

        return redirect(url_for('request_bp.summary_request', request_id=new_request.id))

    return render_template("request.html")

>>>>>>> auth

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
    runner_id = session.get('user_id')

    accepted_jobs = []
    if runner_id:
        accepted_jobs = Request.query.filter_by(status="accepted", runner_id=runner_id).all()
<<<<<<< HEAD

    available_jobs_query = Request.query.filter_by(status="requested")

    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort_by')
    pickup_location = request.args.get('pickup_location')
    dropoff_location = request.args.get('dropoff_location')

    if min_price is not None:
        available_jobs_query = available_jobs_query.filter(Request.price_offer >= min_price)
    if max_price is not None:
        available_jobs_query = available_jobs_query.filter(Request.price_offer <= max_price)

    if pickup_location:
        available_jobs_query = available_jobs_query.filter(Request.pickup_location.ilike(f"%{pickup_location}%"))
    if dropoff_location:
        available_jobs_query = available_jobs_query.filter(Request.dropoff_location.ilike(f"%{dropoff_location}%"))

    if sort_by == "time":
        available_jobs_query = available_jobs_query.order_by(Request.time)
    elif sort_by == "price_offer":
        available_jobs_query = available_jobs_query.order_by(Request.price_offer)
    elif sort_by == "pickup_location":
        available_jobs_query = available_jobs_query.order_by(Request.pickup_location)
    elif sort_by == "dropoff_location":
        available_jobs_query = available_jobs_query.order_by(Request.dropoff_location)

    available_jobs = available_jobs_query.all()
    
=======
    
    available_jobs = Request.query.filter_by(status="requested").all()
>>>>>>> auth
    return render_template("job.html", jobs=available_jobs, accepted_jobs=accepted_jobs)

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

    return redirect(url_for('request_bp.show_jobs'))

@request_bp.route('/login/<int:user_id>')
def log_in(user_id):
    session['user_id'] = user_id
<<<<<<< HEAD
    return f'Logged in as {user_id}'
=======
    return f'Logged in as {user_id}'
>>>>>>> auth
