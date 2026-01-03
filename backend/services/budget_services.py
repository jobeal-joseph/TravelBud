def get_budget_summary(expenses):
    """
    Summarizes expenses by category and calculates the total.
    """
    total = sum(exp.amount for exp in expenses)
    
    # Grouping by category for the chart
    breakdown = {}
    for exp in expenses:
        category = exp.category
        breakdown[category] = breakdown.get(category, 0) + exp.amount
        
    return {
        "total_cost": round(total, 2),
        "breakdown": breakdown,
        "expense_count": len(expenses)
    }