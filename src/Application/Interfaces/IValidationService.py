from abc import ABC, abstractmethod


class IValidationService(ABC):

    @abstractmethod
    def validate_request_data(self, data, required_fields):
        pass

    @abstractmethod
    def validate_userdata(self, username, password, email):
        pass
