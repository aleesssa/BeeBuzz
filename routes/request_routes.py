from flask import Blueprint, flash, jsonify, request, render_template, url_for, redirect, session
from flask_login import current_user, login_required
from extensions import db
from models.request import Request
from datetime import datetime
from models.user import User
from models.rating import Rating

request_bp = Blueprint('request_bp', __name__) # Equivalent to app = Flask(__name__)

@request_bp.route('/')
def request_job():
     return render_template ("request.html")

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

@request_bp.route('/jobs')
def show_jobs():
    runner_id = current_user.id

    accepted_jobs = []
    if runner_id:
        accepted_jobs = Request.query.filter_by(status="accepted", runner_id=runner_id).all()
    
    available_jobs = Request.query.filter_by(status="requested").all()
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
       req.runner_id = current_user.id
    db.session.commit()

    return redirect(url_for('request_bp.show_jobs'))

@request_bp.route('/track/<int:request_id>')
def track_status(request_id):
    req = Request.query.get_or_404(request_id)
    return render_template("deliverystatus.html", request_data=req)

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


@request_bp.route('/rate', methods=['POST'])
@login_required
def rate_request():
    data = request.get_json()
    req = Request.query.get_or_404(data['request_id'])
    score = int(data['score'])
    if not 1 <= score <= 5:
        return jsonify(error='Invalid score'), 400

    rating = Rating.query.filter_by(user_id=current_user.id, request_id=req.id).first()
    if rating:
        rating.score = score
    else:
        rating = Rating(score=score, user=current_user, request=req)
        db.session.add(rating)
    db.session.commit()

    avg = db.session.query(db.func.avg(Rating.score)).filter_by(request_id=req.id).scalar() or 0
    return jsonify(average=round(avg, 2))

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
