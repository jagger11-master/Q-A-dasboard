import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password):
    """Validate password strength"""
    # At least 8 characters, one uppercase, one lowercase, one number
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True

def validate_name(name):
    """Validate name (non-empty and reasonable length)"""
    return bool(name and 2 <= len(name.strip()) <= 100)

def validate_questionnaire_title(title):
    """Validate questionnaire title"""
    return bool(title and 1 <= len(title.strip()) <= 200)

def validate_question_text(text):
    """Validate question text"""
    return bool(text and 1 <= len(text.strip()) <= 1000)