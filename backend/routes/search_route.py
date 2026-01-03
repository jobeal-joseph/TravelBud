from flask import Blueprint, request, jsonify, render_template
from services.search_service import search_cities
from models.expense import Trip, db

# Define the blueprint variable clearly
search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search_page():
    return render_template('city_search.html')

@search_bp.route('/api/cities')
def get_cities():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    return jsonify(search_cities(query))

@search_bp.route('/api/trips/create', methods=['POST'])
def create_trip():
    data = request.json
    try:
        new_trip = Trip(city_name=data['city'], country=data['country'])
        db.session.add(new_trip)
        db.session.commit()
        return jsonify({"trip_id": new_trip.id, "city": new_trip.city_name}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400