# backend/src/middleware/token_verification.py
from functools import wraps
from flask import request, jsonify
import jwt
import os

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
        
        # If no token, return error
        if not token:
            return jsonify({"error": "Authentication token is missing"}), 401
        
        try:
            # Decode the token
            payload = jwt.decode(
                token, 
                os.getenv('JWT_SECRET_KEY'), 
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        
        # Attach user information to the request for further use if needed
        request.user = payload
        
        return f(*args, **kwargs)
    
    return decorated