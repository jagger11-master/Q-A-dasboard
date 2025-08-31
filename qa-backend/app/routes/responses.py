# app/routes/responses.py
from flask import Blueprint, request, jsonify
from app import db
from app.models import Response, Answer, Questionnaire
from app.utils.decorators import jwt_required, role_required
from flask_jwt_extended import get_jwt_identity

responses_bp = Blueprint('responses', __name__)

@responses_bp.route('', methods=['POST'])
@jwt_required()
@role_required('interviewee')
def submit_response():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        questionnaire_id = data.get('questionnaire_id')
        answers = data.get('answers', [])
        
        if not questionnaire_id:
            return jsonify({'error': 'Questionnaire ID is required'}), 400
        
        # Check if questionnaire exists and is active
        questionnaire = Questionnaire.query.filter_by(
            id=questionnaire_id, 
            is_active=True
        ).first()
        
        if not questionnaire:
            return jsonify({'error': 'Questionnaire not found or not active'}), 404
        
        # Check if user has already submitted a response
        existing_response = Response.query.filter_by(
            questionnaire_id=questionnaire_id,
            interviewee_id=current_user['id']
        ).first()
        
        if existing_response:
            return jsonify({'error': 'You have already submitted a response for this questionnaire'}), 409
        
        # Create response
        response = Response(
            questionnaire_id=questionnaire_id,
            interviewee_id=current_user['id']
        )
        db.session.add(response)
        db.session.flush()  # To get the response ID
        
        # Add answers
        for answer_data in answers:
            answer = Answer(
                response_id=response.id,
                question_id=answer_data.get('question_id'),
                answer_text=answer_data.get('answer_text')
            )
            db.session.add(answer)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Response submitted successfully',
            'response_id': response.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@responses_bp.route('/my-responses', methods=['GET'])
@jwt_required()
def get_my_responses():
    try:
        current_user = get_jwt_identity()
        
        responses = Response.query.filter_by(
            interviewee_id=current_user['id']
        ).all()
        
        result = []
        for response in responses:
            result.append({
                'id': response.id,
                'questionnaire_title': response.questionnaire.title,
                'submitted_at': response.submitted_at.isoformat(),
                'question_count': len(response.answers)
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500