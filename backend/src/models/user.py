# backend/src/models/user.py
from src.extensions import db
from sqlalchemy.sql import func
from email_validator import validate_email, EmailNotValidError
import re

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, username, email, password):
        # Validate username
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            raise ValueError("Invalid username. Must be 3-20 characters, alphanumeric or underscore.")
        
        # Validate email
        try:
            valid = validate_email(email)
            self.email = valid.email
        except EmailNotValidError as e:
            raise ValueError(str(e))
        
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }