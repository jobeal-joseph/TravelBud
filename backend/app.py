from flask import Flask, redirect, render_template, url_for
from flask_cors import CORS
from extensions import db
from routes.auth_routes import auth_bp
from routes.search_route import search_bp
from routes.budget_route import budget_bp

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

app.config.from_object('config.Config')

CORS(app)

db.init_app(app)
with app.app_context():
    from models.expense import Expense 
    db.create_all()

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(search_bp)
app.register_blueprint(budget_bp)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)