# backend/src/app.py
from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import extensions and routes
from src.extensions import db, bcrypt
from src.routes.auth import auth_bp
from src.middleware.token_verification import token_required

def create_app():
    app = Flask(__name__)
    
    # CORS configuration
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Sample protected route
    @app.route('/api/dashboard', methods=['GET'])
    @token_required
    def dashboard():
        return {"message": "Welcome to the dashboard!"}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)