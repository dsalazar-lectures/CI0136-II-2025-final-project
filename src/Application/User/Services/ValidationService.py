import re
from src.Application.Interfaces.IValidationService import IValidationService


class ValidationService(IValidationService):
    @staticmethod
    def validate_request_data(data, required_fields):
        # Validate request data
        # Returns: (is_valid, error_response, status_code)
        if not data:
            return False, {"error": "Invalid input"}, 400

        for field in required_fields:
            if field not in data or data[field] is None or data[field] == "":
                return False, {"error": f"Missing field: {field}"}, 400

        return True, None, None

    @staticmethod
    def validate_userdata(username, email):
        if not username or not isinstance(username, str):
            return False, "Username is required"
        if not email or not isinstance(email, str):
            return False, "Email is required"
        if "@" not in email or "." not in email:
            return False, "Invalid email format"
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        return True, None

    @staticmethod
    def validate_password_format(password: str):
        """
        Validates that the password meets security requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one number
        - At least one symbol
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."

        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter."

        if not re.search(r"[0-9]", password):
            return False, "Password must contain at least one number."

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character."

        return True, "Password format is valid."

    @staticmethod
    def validate_email_format(email: str):
        # Validates that the email has a correct format using a regex pattern.
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if re.match(pattern, email):
            return True, "Valid email format"
        return False, "Invalid email format. Example: user@example.com"
