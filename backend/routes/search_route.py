from flask import Blueprint, request, jsonify, render_template
from services.search_service import search_cities

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search_page():
    return render_template('city_search.html')

@search_bp.route('/api/cities')
def get_cities():
    query = request.args.get('q', '')
    return jsonify(search_cities(query))