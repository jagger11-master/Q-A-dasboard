
from app import db, bcrypt
from app.models import User
from app.utils.validators import validate_email, validate_password, validate_name
import uuid

class AuthService:
    @staticmethod
    def register_user(name, email, password, role):
        # Validate inputs
        if not all([validate_name(name), validate_email(email), validate_password(password)]):
            return None, "Invalid input data"
        
        if role not in ['interviewer', 'interviewee']:
            return None, "Invalid role"
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return None, "User already exists"
        
        # Create new user
        try:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(
                id=str(uuid.uuid4()),
                name=name,
                email=email,
                password=hashed_password,
                role=role
            )
            db.session.add(user)
            db.session.commit()
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user, None
        return None, "Invalid credentials"
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)