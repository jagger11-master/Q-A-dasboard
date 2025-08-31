from app import db
from app.models import Questionnaire, Question, Response, Answer
import uuid

class QuestionnaireService:
    @staticmethod
    def create_questionnaire(title, description, questions, created_by):
        try:
            # Create questionnaire
            questionnaire = Questionnaire(
                id=str(uuid.uuid4()),
                title=title,
                description=description,
                created_by=created_by
            )
            db.session.add(questionnaire)
            db.session.flush()  # Get the ID without committing
            
            # Add questions
            for i, question_data in enumerate(questions):
                question = Question(
                    id=str(uuid.uuid4()),
                    questionnaire_id=questionnaire.id,
                    question_text=question_data.get('question_text'),
                    question_type=question_data.get('question_type', 'text'),
                    options=question_data.get('options'),
                    order=i
                )
                db.session.add(question)
            
            db.session.commit()
            return questionnaire, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def get_questionnaires_for_user(user_id, role):
        if role == 'interviewer':
            return Questionnaire.query.filter_by(created_by=user_id).all()
        else:
            return Questionnaire.query.filter_by(is_active=True).all()
    
    @staticmethod
    def get_questionnaire_with_questions(questionnaire_id, role):
        questionnaire = Questionnaire.query.get(questionnaire_id)
        if not questionnaire:
            return None, "Questionnaire not found"
        
        # Check if interviewee is accessing and questionnaire is active
        if role == 'interviewee' and not questionnaire.is_active:
            return None, "Questionnaire not available"
        
        return questionnaire, None
    
    @staticmethod
    def submit_response(questionnaire_id, interviewee_id, answers):
        try:
            # Check if questionnaire exists and is active
            questionnaire = Questionnaire.query.filter_by(
                id=questionnaire_id, 
                is_active=True
            ).first()
            
            if not questionnaire:
                return None, "Questionnaire not found or not active"
            
            # Check if user has already submitted a response
            existing_response = Response.query.filter_by(
                questionnaire_id=questionnaire_id,
                interviewee_id=interviewee_id
            ).first()
            
            if existing_response:
                return None, "You have already submitted a response for this questionnaire"
            
            # Create response
            response = Response(
                id=str(uuid.uuid4()),
                questionnaire_id=questionnaire_id,
                interviewee_id=interviewee_id
            )
            db.session.add(response)
            db.session.flush()
            
            # Add answers
            for answer_data in answers:
                answer = Answer(
                    id=str(uuid.uuid4()),
                    response_id=response.id,
                    question_id=answer_data.get('question_id'),
                    answer_text=answer_data.get('answer_text')
                )
                db.session.add(answer)
            
            db.session.commit()
            return response, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)