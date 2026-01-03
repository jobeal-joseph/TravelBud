from flask_sqlalchemy import SQLAlchemy
from app import db 

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, nullable=False) # Link to the trip
    category = db.Column(db.String(50), nullable=False) # e.g., Transport, Food, Stay
    description = db.Column(db.String(200))
    amount = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "description": self.description,
            "amount": self.amount
        }