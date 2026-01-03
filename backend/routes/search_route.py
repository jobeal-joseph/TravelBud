from flask import Blueprint, request, jsonify, render_template
from services.search_service import search_cities

search_bp = Blueprint("search", __name__, url_prefix="/api/search")

@search_bp.route("/view")
def city_search_page():
    return render_template("city_search.html")

@search_bp.route("/cities")
def get_cities():
    q = request.args.get("q", "")
    if not q:
        return jsonify([])
    results = search_cities(q)
    return jsonify(results)