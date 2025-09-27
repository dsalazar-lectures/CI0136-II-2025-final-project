class ValidationService:

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
    def validate_userdata(self, username, password, email):
        if not username or not isinstance(username, str):
            return False, "Username is required"
        if not password or not isinstance(password, str):
            return False, "Password is required"
        if not email or not isinstance(email, str):
            return False, "Email is required"
        if "@" not in email or "." not in email:
            return False, "Invalid email format"
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        return True, None
