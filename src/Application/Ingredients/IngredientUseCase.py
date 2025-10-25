from typing import List, Optional
from Infrastructure.Ingredients.IngredientRepository \
                                                    import IngredientRepository
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

    def get_ingredient_by_name(
                           self, ingredient_name: str) -> Optional[Ingredient]:

        """Get a specific ingredient by its name."""
        return self.repository.get_by_name(ingredient_name)

    def create_ingredient(self, name, categories, substitutes, components, recipe_count = 0):
        """Create a new ingredient"""
        return self.repository.create_ingredient(name, categories, substitutes, components, recipe_count)
    
    def add_recipe(self, ingredient_id: int):
        """Add a recipe to an ingredient's recipe count"""
        return self.repository.add_recipe(ingredient_id)
    
    def update_categories(self, ingredient_id: int, categories):
        """Update an ingredient's categories"""
        return self.repository.update_ingredient_categories(ingredient_id, categories)
    
    def update_substitutes(self, ingredient_id: int, substitutes):
        """Update an ingredient's substitutes"""
        return self.repository.update_ingredient_substitutes(ingredient_id, substitutes)
    
    def update_components(self, ingredient_id: int, components):
        """Update an ingredient's components"""
        return self.repository.update_ingredient_components(ingredient_id, components)
    
    def delete_ingredient(self, ingredient_id: int):
        """Delete an ingredient from the ingredient dictionary"""
        return self.repository.delete_ingredient(ingredient_id)


# Create a singleton instance to be imported by the routes
ingredient_service = IngredientUseCase()
