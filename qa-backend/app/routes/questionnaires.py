# app/routes/questionnaires.py
from flask import Blueprint, request, jsonify
from app import db
from app.models import Questionnaire, Question, Response, Answer, User
from app.utils.decorators import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity
questionnaires_bp = Blueprint('questionnaires', __name__)
@questionnaires_bp.route('', methods=['POST'])
@jwt_required()
@role_required('interviewer')
def create_questionnaire():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        title = data.get('title')
        description = data.get('description')
        questions = data.get('questions', [])
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        # Create questionnaire
        questionnaire = Questionnaire(
            title=title,
            description=description,
            created_by=current_user['id']
        )
        db.session.add(questionnaire)
        db.session.flush()  # To get the questionnaire ID
        
        # Add questions
        for i, q_data in enumerate(questions):
            question = Question(
                questionnaire_id=questionnaire.id,
                question_text=q_data.get('question_text'),
                question_type=q_data.get('question_type', 'text'),
                options=q_data.get('options'),
                order=i
            )
            db.session.add(question)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Questionnaire created successfully',
            'questionnaire_id': questionnaire.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@questionnaires_bp.route('', methods=['GET'])
@jwt_required()
def get_questionnaires():
    try:
        current_user = get_jwt_identity()
        
        if current_user['role'] == 'interviewer':
            # Interviewers see their own questionnaires
            questionnaires = Questionnaire.query.filter_by(
                created_by=current_user['id']
            ).all()
        else:
            # Interviewees see all active questionnaires
            questionnaires = Questionnaire.query.filter_by(
                is_active=True
            ).all()
        
        result = []
        for q in questionnaires:
            result.append({
                'id': q.id,
                'title': q.title,
                'description': q.description,
                'created_at': q.created_at.isoformat(),
                'question_count': len(q.questions)
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questionnaires_bp.route('/<questionnaire_id>', methods=['GET'])
@jwt_required()
def get_questionnaire(questionnaire_id):
    try:
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        
        # Check if interviewee is accessing and questionnaire is active
        current_user = get_jwt_identity()
        if current_user['role'] == 'interviewee' and not questionnaire.is_active:
            return jsonify({'error': 'Questionnaire not available'}), 403
        
        questions = []
        for q in questionnaire.questions:
            questions.append({
                'id': q.id,
                'question_text': q.question_text,
                'question_type': q.question_type,
                'options': q.options,
                'order': q.order
            })
        
        # Sort questions by order
        questions.sort(key=lambda x: x['order'])
        
        return jsonify({
            'id': questionnaire.id,
            'title': questionnaire.title,
            'description': questionnaire.description,
            'created_at': questionnaire.created_at.isoformat(),
            'questions': questions
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questionnaires_bp.route('/<questionnaire_id>/responses', methods=['GET'])
@jwt_required()
@role_required('interviewer')
def get_questionnaire_responses(questionnaire_id):
    try:
        current_user = get_jwt_identity()
        questionnaire = Questionnaire.query.filter_by(
            id=questionnaire_id, 
            created_by=current_user['id']
        ).first_or_404()
        
        responses = Response.query.filter_by(
            questionnaire_id=questionnaire_id
        ).all()
        
        result = []
        for response in responses:
            answers = []
            for answer in response.answers:
                answers.append({
                    'question_id': answer.question_id,
                    'question_text': answer.question.question_text,
                    'answer_text': answer.answer_text
                })
            
            result.append({
                'response_id': response.id,
                'interviewee_name': response.interviewee.name,
                'interviewee_email': response.interviewee.email,
                'submitted_at': response.submitted_at.isoformat(),
                'answers': answers
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Test endpoint to verify JWT functionality
@questionnaires_bp.route('/test', methods=['GET'])
@jwt_required()
def test_jwt():
    current_user = get_jwt_identity()
    return jsonify({'message': 'JWT is working!', 'user': current_user}), 200