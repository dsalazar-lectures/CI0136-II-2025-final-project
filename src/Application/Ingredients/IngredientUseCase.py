from typing import List, Optional
from Infrastructure.Ingredients.IngredientRepository import IngredientRepository
from Model.Ingredients.Ingredients import Ingredient

class IngredientUseCase:
    def __init__(self):
        self.repository = IngredientRepository()
    
    def get_all_ingredients(self) -> List[Ingredient]:
        """Get all ingredients ordered alphabetically."""
        return self.repository.get_all()
    
    def get_ingredient_by_id(self, ingredient_id: int) -> Optional[Ingredient]:
        """Get a specific ingredient by its ID."""
        return self.repository.get_by_id(ingredient_id)

# Create a singleton instance to be imported by the routes
ingredient_service = IngredientUseCase()
