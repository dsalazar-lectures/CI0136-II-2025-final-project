class UserResponseDTO:
    """DTO solo para responses, sin datos sensibles"""

    def __init__(self, id, username, email, role="user"):
        self.id = id
        self.username = username
        self.email = email
        self.role = role

    def to_dict(self):
        return self.__dict__
