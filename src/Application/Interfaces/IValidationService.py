from abc import ABC, abstractmethod

class IValidationService(ABC):

    @abstractmethod
    def validate_request_data(self, data, required_fields):
        pass

    @abstractmethod
    def validate_username(self, username):
        pass

    @abstractmethod
    def validate_email(self, email):
        pass

    @abstractmethod
    def validate_password(self, password):
        pass

    @abstractmethod
    def validate_userdata(self, username, password, email):
        pass
