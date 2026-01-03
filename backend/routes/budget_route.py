from flask import Blueprint, request, jsonify, render_template
from models.expense import Expense, db

budget_bp = Blueprint('budget', __name__, url_prefix='/api/budget')

@budget_bp.route('/view')
def budget_view():
    return render_template('budget_view.html')

@budget_bp.route('/add', methods=['POST'])
def add_expense():
    data = request.json
    try:
        new_expense = Expense(
            trip_id=1, # Default trip for hackathon demo
            category=data['category'],
            description=data['description'],
            amount=float(data['amount'])
        )
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({"message": "Expense recorded"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@budget_bp.route('/summary')
def get_summary():
    expenses = Expense.query.all()
    total = sum(e.amount for e in expenses)
    
    # Generate the breakdown for the UI Chart
    breakdown = {}
    for e in expenses:
        breakdown[e.category] = breakdown.get(e.category, 0) + e.amount
        
    return jsonify({
        "total": round(total, 2),
        "breakdown": breakdown,
        "history": [e.to_dict() for e in expenses]
    })