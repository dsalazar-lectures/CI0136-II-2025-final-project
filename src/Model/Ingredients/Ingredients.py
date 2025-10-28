from abc import ABC, abstractmethod
from typing import List, Dict


class Ingredient(ABC):
    def __init__(self) -> None:
        self.id = None
        self.name = None
        self.categories = []
        self.substitutes = []
        self.recipe_count = 0

    def get_id(self):
        return self.id

    def __str__(self) -> str:
        return self.name

    def _format_fields(self) -> None:
        """Replace all spaces with hyphens"""
        self.name = self.name.replace(" ", "-")
        for index in range(len(self.categories)):
            self.categories[index] = self.categories[index].replace(" ", "-")
        for index in range(len(self.substitutes)):
            self.substitutes[index] = self.substitutes[index].replace(" ", "-")
        
    def get_recipe_count(self) -> int:
        return self.recipe_count

    def has_substitutes(self) -> bool:
        return len(self.substitutes) > 0

    def add_recipe(self) -> None:
        self.recipe_count = self.recipe_count + 1

    def update_categories(self, categories: List[str]) -> None:
        self.categories = list(categories or [])
        self._format_fields()

    def update_substitutes(self, substitutes: List[str]) -> None:
        self.substitutes = list(substitutes or [])
        self._format_fields()

    @abstractmethod
    def is_base_ingredient(self) -> bool:
        pass

    @abstractmethod
    def to_json(self) -> Dict:
        pass
