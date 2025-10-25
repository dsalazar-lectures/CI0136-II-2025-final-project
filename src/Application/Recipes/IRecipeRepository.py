from abc import ABC, abstractmethod

class IRecipeRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, recipe_id):
        pass

    @abstractmethod
    def find_by_ingredient(self, ingredient):
        pass

    @abstractmethod
    def add_recipe(self, recipe_data):
        pass

    @abstractmethod
    def delete_if_owned(self, recipe_id, username):
        pass

    @abstractmethod
    def update_if_owned(self, recipe_id, username, updates):
        pass

    @abstractmethod
    def find_by_category(self, category):
        pass