from flask import Blueprint, render_template, request, jsonify, session
from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        data = request.json

        if not data.get("email") or not data.get("password"):
            return jsonify({"error": "Missing fields"}), 400

        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already exists"}), 409

        user = User(
            name=data.get("name", "User"),
            email=data["email"]
        )
        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Signup successful"}), 201
    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=["GET","POST"])
def login():
   if request.method == "POST": 
     data = request.json
     user = User.query.filter_by(email=data.get("email")).first()

     if not user or not user.check_password(data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

     session["user_id"] = user.id
     return jsonify({"message": "Login successful"})
   return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})
