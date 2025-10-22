from src.Application.Interfaces.IValidationService import IValidationService
import re

class ValidationService(IValidationService):

    @staticmethod
    def validate_request_data(data, required_fields):
        # Validate request data
        # Returns: (is_valid, error_response, status_code)
        if not data:
            return False, {'error': 'Invalid input'}, 400

        for field in required_fields:
            if field not in data or data[field] is None or data[field] == "":
                return False, {'error': f'Missing field: {field}'}, 400

        return True, None, None

    @staticmethod
    def validate_username(username: str):
        if not username or not isinstance(username, str):
            return False, "Username is required"
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        return True, None

    @staticmethod
    def validate_email(email: str):
        if not email or not isinstance(email, str):
            return False, "Email is required"
        if "@" not in email or "." not in email:
            return False, "Invalid email format"
        return True, None
    
    @staticmethod
    def validate_password(password: str):
        """
        Password policy:
          - Minimum length: 8
          - At least one digit [0-9]
          - At least one uppercase letter [A-Z]
          - At least one special character from: # $ % .
        """
        if not password or not isinstance(password, str):
            return False, "Password is required"

        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r"\d", password):
            return False, "Password must include at least one number"
        if not re.search(r"[A-Z]", password):
            return False, "Password must include at least one uppercase letter"
        if not re.search(r"[#\$%\.]", password):
            return False, "Password must include at least one special character (#, $, %, .)"
        return True, None
    
    @staticmethod
    def validate_userdata(username, password, email):

        ok, msg = ValidationService.validate_username(username)
        if not ok:
            return False, msg

        ok, msg = ValidationService.validate_email(email)
        if not ok:
            return False, msg

        ok, msg = ValidationService.validate_password(password)
        if not ok:
            return False, msg

        return True, None