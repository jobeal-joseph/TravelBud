from flask import Blueprint, request, jsonify, render_template
from extensions import db
from models.expense import Expense, Trip

budget_bp = Blueprint('budget', __name__)

@budget_bp.route('/budget')
def budget_view():
    return render_template('budget_view.html')

@budget_bp.route('/api/budget/add', methods=['POST'])
def add_expense():
    data = request.json
    try:
        # Check if trip_id exists in the Trip table first
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
        print(f"DATABASE ERROR: {e}") # This will show the error in your terminal
        return jsonify({"error": str(e)}), 400

@budget_bp.route('/api/budget/summary')
def get_summary():
    # We get the trip_id from the URL query string
    t_id = request.args.get('trip_id')
    if not t_id:
        return jsonify({"total": 0, "breakdown": {}})

    expenses = Expense.query.filter_by(trip_id=t_id).all()
    total = sum(e.amount for e in expenses)
    
    breakdown = {}
    for e in expenses:
        breakdown[e.category] = breakdown.get(e.category, 0) + e.amount
        
    return jsonify({
        "total": round(total, 2),
        "breakdown": breakdown
    })