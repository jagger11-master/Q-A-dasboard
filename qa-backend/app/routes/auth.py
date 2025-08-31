# app/routes/auth.py
from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User
from app.utils.decorators import role_required
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        
        # Validation
        if not all([name, email, password, role]):
            return jsonify({'error': 'All fields are required'}), 400
        
        if role not in ['interviewer', 'interviewee']:
            return jsonify({'error': 'Invalid role'}), 400
        
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'User already exists'}), 409
        
        # Create user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        
        return jsonify({
            'message': 'User created successfully',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity={'id': user.id, 'role': user.role})
            return jsonify({
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'role': user.role
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500