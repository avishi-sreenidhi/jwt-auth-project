# backend/src/routes/auth.py
from flask import Blueprint, request, jsonify
from src.models.user import User
from src.extensions import db, bcrypt
import jwt
import datetime
import os

auth_bp = Blueprint('auth', __name__)

def generate_token(user):
    """Generate JWT token for a user"""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # Token expires in 2 hours
    }
    return jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == data['username']) | (User.email == data['email'])
        ).first()
        
        if existing_user:
            return jsonify({"error": "Username or email already exists"}), 409
        
        # Hash password
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        
        # Create new user
        new_user = User(
            username=data['username'], 
            email=data['email'], 
            password=hashed_password
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate token
        token = generate_token(new_user)
        
        return jsonify({
            "message": "User registered successfully",
            "user": new_user.to_dict(),
            "token": token
        }), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Registration failed", "details": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = generate_token(user)
        return jsonify({
            "message": "Login successful",
            "user": user.to_dict(),
            "token": token
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/protected', methods=['GET'])
def protected_route():
    # JWT token verification middleware will handle this before reaching this route
    return jsonify({"message": "Access to protected route granted"}), 200