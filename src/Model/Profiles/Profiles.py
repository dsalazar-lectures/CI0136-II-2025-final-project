from src.Model.Profiles.Roles import Role


class Profile:
    def __init__(
        self,
        user_id,
        favorite_foods=None,
        unfavorite_foods=None,
        favorite_menus=None,
        role=Role.USER,
    ):
        self.user_id = user_id
        self.favorite_foods = favorite_foods if favorite_foods is not None else []
        self.unfavorite_foods = unfavorite_foods if unfavorite_foods is not None else []
        self.favorite_menus = favorite_menus if favorite_menus is not None else []
        self.role = role

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "favorite_foods": self.favorite_foods,
            "unfavorite_foods": self.unfavorite_foods,
            "favorite_menus": self.favorite_menus,
            "role": self.role,
        }
