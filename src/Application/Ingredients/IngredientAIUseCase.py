from typing import Dict

from src.Application.Ingredients.IngredientUseCase import ingredient_service
from src.Infrastructure.Ingredients.DeepSeekClient import DeepSeekClient


class IngredientAIUseCase:
    """
    Application use case to get AI-generated messages
    with ingredient substitutes using DeepSeek
    """

    def __init__(self) -> None:
        self._ingredient_service = ingredient_service
        self._ai_client = DeepSeekClient()

    def get_ai_substitutes_message(self, ingredient_name: str) -> Dict:
        """
        Get a message from DeepSeek suggesting substitutes
        for the given ingredient name

        """
        ingredient = self._ingredient_service.get_ingredient_by_name(ingredient_name)
        if ingredient is None:
            return {
                "status_code": 404,
                "body": {"error": "Ingredient not found"},
            }

        message, error = self._ai_client.get_natural_substitute_message(
            ingredient_name=ingredient.name,
            categories=list(ingredient.categories),
            current_substitutes=list(ingredient.substitutes),
            language="es",
        )

        if error is not None:
            return {
                "status_code": 503,
                "body": {
                    "error": "DeepSeek service is not available",
                    "details": error,
                },
            }

        return {
            "status_code": 200,
            "body": {
                "ingredient": ingredient.to_json(),
                "ai_message": message,
            },
        }


# singleton instance to be imported by the routes
ingredient_ai_service = IngredientAIUseCase()
