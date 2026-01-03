from flask import Flask, redirect, render_template, url_for
from flask_cors import CORS
from extensions import db
from routes.auth_routes import auth_bp




app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.config.from_object('config.Config')

CORS(app)

db.init_app(app)
with app.app_context():
    db.create_all()
app.register_blueprint(auth_bp , url_prefix='/auth')


print(app.url_map)
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/create_trip')
def create_trip():
    return render_template('create_trip.html')

if __name__ == '__main__':
    app.run(debug=True)

