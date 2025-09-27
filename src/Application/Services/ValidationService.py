from flask import jsonify


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
