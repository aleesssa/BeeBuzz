from flask import Blueprint, flash, jsonify, request, render_template, url_for, redirect, session
from flask_login import current_user, login_required
from flask_socketio import SocketIO, emit, join_room
from extensions import db, socketio
from models.request import Request
from datetime import datetime
from models.user import User
from models.rating import Rating
from sqlalchemy import and_, or_
from utils.system_utils import system_update

request_bp = Blueprint('request_bp', __name__) # Equivalent to app = Flask(__name__)

@request_bp.route('/')
def request_job():
     return render_template ("request.html")

# Post Request 
@request_bp.route('/req', methods=['GET','POST'])
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
            time=request.form.get("time"),
            pickup_location=request.form.get("pickup"),
            dropoff_location=request.form.get("dropoff"),
            notes=request.form.get("notes"),
            created_at=datetime.utcnow(),
            client_id=current_user.id,
            runner_id=None,
            status='requested'
        )
        db.session.add(new_request)
        db.session.commit()

        return redirect(url_for('request_bp.summary_request', request_id=new_request.id))
    
    return render_template("request.html")

# Edit Request
@request_bp.route('/edit/<int:request_id>')
def edit_request(request_id):
    req = Request.query.get_or_404(request_id)
    return render_template("update.html",request=req)

@request_bp.route('/update/<int:request_id>', methods=['POST'])
def update_request(request_id):
    req = Request.query.get_or_404(request_id)
    
    if req.client_id != current_user.id:
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
@login_required
def summary_request(request_id):
    req = Request.query.get_or_404(request_id)

    avg = db.session.query(db.func.avg(Rating.score))\
           .filter_by(request_id=req.id).scalar() or 0
    req.average_rating = round(avg, 1)

    rating = Rating.query.filter_by(
        request_id=req.id,
        user_id=current_user.id
    ).first()
    req.user_rating = rating.score if rating else None

    return render_template(
        'summaryreq.html',
        data=req,
        request_id=req.id,
        user_rating=req.user_rating
    )

@request_bp.route('/cancelled/<int:request_id>', methods=['POST'])
def cancel_request(request_id):
    req = Request.query.get_or_404(request_id)
    if req.client_id != current_user.id:
        return "Unauthorized", 403

    req.status = "cancelled"
    req.updated_at = datetime.utcnow()
    db.session.commit()

    return "Your order has been cancelled."

# Show List of Jobs
@request_bp.route('/jobs')
def show_jobs():
    active_ids = [r.id for r in Request.query.filter_by(runner_id=current_user.id, status='on the way').all()]
    runner_id = current_user.id

    accepted_jobs = []
    if runner_id:
        accepted_jobs = Request.query.filter(
            and_(
                Request.runner_id == runner_id,
                or_(
                    Request.status == "accepted",
                    Request.status == "picked up",
                    Request.status == "on the way")
                )
                ).all()
        
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
    
    return render_template("job.html", jobs=available_jobs, accepted_jobs=accepted_jobs, active_ids=active_ids)

@request_bp.route('/jobs/details/<int:request_id>')
def view_details(request_id):
    req = Request.query.get_or_404(request_id)
    return render_template("request_details.html", job_request=req)

# Accept Job
@request_bp.route('/jobs/accept/<int:request_id>', methods=['POST'])
def accept_jobs(request_id):
    req = Request.query.get_or_404(request_id)

    if req.status == "requested":
       req.status = "accepted"
       req.runner_id = current_user.id
    db.session.commit()
    system_update('Rider has accepted your request!', request_id=request_id)

    return redirect(url_for('request_bp.show_jobs'))

# Track/Update Status Order
@request_bp.route('/track/<int:request_id>')
def track_status(request_id):
    user_role = User.query.filter_by(id=current_user.id).first().role
    active_ids = [r.id for r in Request.query.filter_by(runner_id=current_user.id, status='on the way').all()]
    req = Request.query.get_or_404(request_id)
    return render_template("deliverystatus.html", request_data=req, request_id=request_id, active_ids=active_ids, user_role=user_role)

@request_bp.route('/update_request/<int:request_id>', methods=['POST'])
def update_delivery(request_id):
    req = Request.query.get_or_404(request_id)

    new_status = request.form.get('status')

    if new_status:
        req.status = new_status
        req.updated_at = datetime.utcnow()
        db.session.commit()
    
    return redirect(url_for('request_bp.track_status', request_id=request_id))


@request_bp.route('/history')
@login_required
def history():
    user_history = Request.query.filter_by(client_id=current_user.id)\
                        .order_by(Request.created_at.desc()).all()

    for req in user_history:
        avg = db.session.query(db.func.avg(Rating.score))\
               .filter_by(request_id=req.id).scalar() or 0
        req.average_rating = round(avg, 1)

        rating = Rating.query.filter_by(
            request_id=req.id,
            user_id=current_user.id
        ).first()
        req.user_rating = rating.score if rating else None

    return render_template('history.html', user_history=user_history)



@request_bp.route('/complete/<int:request_id>', methods=['POST'])
@login_required
def complete_request(request_id):
    req = Request.query.get_or_404(request_id)
    if req.client_id != current_user.id:
        return "Unauthorized", 403
    
    req.status = 'completed'
    req.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Request marked as completed!', 'success')
    return redirect(url_for('request_bp.summary_request', request_id=request_id))

@socketio.on("join_tracking")
def handle_join_tracking(data):
    join_room(str(data["request_id"]))


@socketio.on("runner_location")
def handle_runner_location(data): 
    for request_id in data["activeRequests"]:
        emit("update_runner_location", {
            "request_id": request_id,
            "user_id": data["user_id"],
            "lat": data["lat"],
            "lng": data["lng"]
        }, room=str(request_id))