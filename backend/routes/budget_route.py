from flask import Blueprint, request, jsonify, render_template
from extensions import db
from models.expense import Expense, Trip
from services.activity_service import get_activities # Ensure this file exists!

budget_bp = Blueprint('budget', __name__)

@budget_bp.route('/budget')
def budget_view():
    return render_template('budget_view.html')

@budget_bp.route('/api/budget/add', methods=['POST'])
def add_expense():
    data = request.json
    try:
        new_exp = Expense(
            trip_id=int(data.get('trip_id')),
            category=data['category'],
            description=data['description'],
            amount=float(data['amount'])
        )
        db.session.add(new_exp)
        db.session.commit()
        return jsonify({"message": "Expense saved"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@budget_bp.route('/api/budget/summary')
def get_summary():
    t_id = request.args.get('trip_id')
    if not t_id or t_id == "null":
        return jsonify({"total": 0, "breakdown": {}, "recent": [], "activities": []})

    try:
        # 1. Get Trip Info
        trip = Trip.query.get(t_id)
        if not trip:
             return jsonify({"error": "Trip not found"}), 404
        
        # 2. Get Expenses
        expenses = Expense.query.filter_by(trip_id=t_id).all()
        total = sum(e.amount for e in expenses)
        
        breakdown = {}
        for e in expenses:
            breakdown[e.category] = breakdown.get(e.category, 0) + e.amount
            
        recent = [{"category": e.category, "description": e.description, "amount": e.amount} 
                  for e in expenses[-5:]]
        
        # 3. Get Activities (Wrapped in try-except to prevent 500 error)
        activities = []
        try:
            activities = get_activities(trip.city_name)
        except Exception as e:
            print(f"Activity Service Failed: {e}")
            activities = [] # Return empty list instead of crashing

        return jsonify({
            "city": trip.city_name,
            "total": round(total, 2),
            "breakdown": breakdown,
            "recent": recent[::-1],
            "activities": activities
        })
    except Exception as e:
        print(f"General Summary Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500