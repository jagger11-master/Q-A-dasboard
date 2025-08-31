# models.py
from app import db  # Import the shared db instance from app
from datetime import datetime
import uuid

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'interviewer' or 'interviewee'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    questionnaires = db.relationship('Questionnaire', backref='creator', lazy=True)
    responses = db.relationship('Response', backref='interviewee', lazy=True)

class Questionnaire(db.Model):
    __tablename__ = 'questionnaires'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    questions = db.relationship('Question', backref='questionnaire', lazy=True, cascade='all, delete-orphan')
    responses = db.relationship('Response', backref='questionnaire', lazy=True, cascade='all, delete-orphan')

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    questionnaire_id = db.Column(db.String(36), db.ForeignKey('questionnaires.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default='text')  # 'text', 'multiple_choice', etc.
    options = db.Column(db.JSON)  # For multiple choice questions
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Response(db.Model):
    __tablename__ = 'responses'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    questionnaire_id = db.Column(db.String(36), db.ForeignKey('questionnaires.id'), nullable=False)
    interviewee_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    answers = db.relationship('Answer', backref='response', lazy=True, cascade='all, delete-orphan')

class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    response_id = db.Column(db.String(36), db.ForeignKey('responses.id'), nullable=False)
    question_id = db.Column(db.String(36), db.ForeignKey('questions.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    
    # Relationship
    question = db.relationship('Question', backref='answers')