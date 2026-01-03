from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, Trip, City, Activity

trips_bp = Blueprint('trips', __name__)

# ------------------ TRIP ------------------

@trips_bp.route('/api/trips', methods=['POST'])
@login_required
def create_trip():
    data = request.form
    trip = Trip(
        user_id=current_user.id,
        title=data['title'],
        start_date=data.get('start_date'),
        end_date=data.get('end_date')
    )
    db.session.add(trip)
    db.session.commit()
    return redirect(url_for('trips.itinerary_builder', trip_id=trip.id))


@trips_bp.route('/api/trips')
@login_required
def list_trips():
    trips = Trip.query.filter_by(user_id=current_user.id).all()
    return render_template('my_trips.html', trips=trips)


@trips_bp.route('/api/trips/<int:trip_id>', methods=['DELETE'])
@login_required
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(trip)
    db.session.commit()
    return jsonify({"message": "Trip deleted"})

# ------------------ CITY ------------------

@trips_bp.route('/api/trips/<int:trip_id>/cities', methods=['POST'])
@login_required
def add_city(trip_id):
    name = request.json['name']
    count = City.query.filter_by(trip_id=trip_id).count()
    city = City(trip_id=trip_id, name=name, order_index=count)
    db.session.add(city)
    db.session.commit()
    return jsonify({"id": city.id, "name": city.name})


@trips_bp.route('/api/cities/<int:city_id>/move-up', methods=['POST'])
@login_required
def move_city_up(city_id):
    city = City.query.get_or_404(city_id)
    prev_city = City.query.filter(
        City.trip_id == city.trip_id,
        City.order_index == city.order_index - 1
    ).first()

    if prev_city:
        city.order_index, prev_city.order_index = prev_city.order_index, city.order_index
        db.session.commit()

    return jsonify({"success": True})


@trips_bp.route('/api/cities/<int:city_id>/move-down', methods=['POST'])
@login_required
def move_city_down(city_id):
    city = City.query.get_or_404(city_id)
    next_city = City.query.filter(
        City.trip_id == city.trip_id,
        City.order_index == city.order_index + 1
    ).first()

    if next_city:
        city.order_index, next_city.order_index = next_city.order_index, city.order_index
        db.session.commit()

    return jsonify({"success": True})

# ------------------ ACTIVITY ------------------

@trips_bp.route('/api/cities/<int:city_id>/activities', methods=['POST'])
@login_required
def add_activity(city_id):
    data = request.json
    activity = Activity(
        city_id=city_id,
        name=data['name'],
        description=data.get('description', ''),
        cost=data.get('cost', 0)
    )
    db.session.add(activity)
    db.session.commit()
    return jsonify({"id": activity.id, "name": activity.name})


@trips_bp.route('/api/activities/<int:activity_id>', methods=['DELETE'])
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    db.session.delete(activity)
    db.session.commit()
    return jsonify({"success": True})

# ------------------ UI ------------------

@trips_bp.route('/trips/<int:trip_id>')
@login_required
def itinerary_builder(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    return render_template('itinerary_builder.html', trip=trip)
