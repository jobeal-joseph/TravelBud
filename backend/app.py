from flask import Flask, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Initialize DB here so models can import it
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/js')

    app.config.from_object('config.Config')
    
    # Initialize plugins
    CORS(app)
    db.init_app(app)

    # 1. Import and Register blueprints
    from routes.search_route import search_bp 
    from routes.budget_route import budget_bp 
    
    app.register_blueprint(search_bp)
    app.register_blueprint(budget_bp)

    # Create tables automatically for the demo
    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return render_template('login.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)