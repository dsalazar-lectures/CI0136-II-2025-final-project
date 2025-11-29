from typing import List, Optional
from src.Infrastructure.Ingredients.IngredientRepository import IngredientRepository
from src.Model.Ingredients.Ingredients import Ingredient
from src.Application.Interfaces.IExternalIngredientProvider import (
    IExternalIngredientProvider,
)


class IngredientUseCase:
    def __init__(
        self,
        repository: IngredientRepository,
        external_providers: Optional[List[IExternalIngredientProvider]] = None
    ):
        self.repository = repository
        self.external_providers = external_providers or []

    def get_all_ingredients(self) -> List[Ingredient]:
        """Get all ingredients ordered alphabetically."""
        return self.repository.get_all()

    def get_ingredient_by_id(self, ingredient_id: int) -> Optional[Ingredient]:
        """Get a specific ingredient by its ID."""
        return self.repository.get_by_id(ingredient_id)

    def get_ingredient_by_name(self, ingredient_name: str) -> Optional[Ingredient]:
        """Busca localmente, luego externamente si no lo encuentra."""
        local_result = self.repository.get_by_name(ingredient_name)
        if local_result:
            return local_result
        
        results = [
            provider.search_ingredient(ingredient_name)
            for provider in self.external_providers
            if provider is not None
        ]
        
        valid_results = [r for r in results if r is not None]

        if not valid_results:
            return None

        base = valid_results[0]
        combined_categories = set(base.categories)
        combined_substitutes = set(base.substitutes)
        
        for result in valid_results[1:]:
            combined_categories.update(result.categories)
            combined_substitutes.update(result.substitutes)

        self.repository.create_ingredient(
            name=base.name,
            categories=list(combined_categories),
            substitutes=list(combined_substitutes),
            components=getattr(base, "components", []) or [],
            recipe_count=getattr(base, "recipe_count", 0) or 0,
        )
        new_id = self.repository._next_id - 1
        return self.repository.get_by_id(new_id)
        
    def create_ingredient(
        self, name, categories, substitutes, components, recipe_count=0
    ):
        """Create a new ingredient"""
        return self.repository.create_ingredient(
            name, categories, substitutes, components, recipe_count
        )

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


try:
    from .IngredientInjector import ingredient_service_instance as ingredient_service
except ImportError:
    # Esto manejará el error si la importación falla (ej. durante pruebas)
    print("FATAL ERROR: Ingredient service dependency injection failed.")
    ingredient_service = None
