from flask import Blueprint, request, jsonify, render_template
from extensions import db
from models.expense import Expense

budget_bp = Blueprint('budget', __name__)

@budget_bp.route('/budget')
def budget_view():
    return render_template('budget_view.html')

@budget_bp.route('/api/budget/add', methods=['POST'])
def add_expense():
    data = request.json
    new_expense = Expense(
        category=data['category'],
        description=data['description'],
        amount=float(data['amount'])
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Success"}), 201

@budget_bp.route('/api/budget/summary')
def get_summary():
    expenses = Expense.query.all()
    total = sum(e.amount for e in expenses)
    breakdown = {e.category: sum(exp.amount for exp in expenses if exp.category == e.category) for e in expenses}
    return jsonify({"total": round(total, 2), "breakdown": breakdown})