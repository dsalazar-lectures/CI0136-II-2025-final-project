from src.Database.Recipes.IExternalRecipeSource import IExternalRecipeSource
from src.Database.Recipes.TheMealDBService import TheMealDBService


class TheMealDBAdapter(IExternalRecipeSource):

    def __init__(self):
        self.service = TheMealDBService()

    def get_raw_data(self):
        """Obtains API recipes"""
        return self.service.obtain_recipes("")

    def parse_recipe(self, meal):
        """Adapts API recipe to recipe model"""
        categories = self._extract_categories(meal)
        ingredients = self._extract_ingredients(meal)

        return {
            "id": meal.get("idMeal"),
            "name": meal.get("strMeal"),
            "categories": repr(categories),
            "ingredients": repr(ingredients),
            "duration": None,
            "instructions": meal.get("strInstructions"),
            "portions": 1,
            "author": "TheMealDB",
            "calificationsSumatory": 0,
            "calificationsAmount": 0,
            "usersUsedRecipe": 0,
        }

    def _extract_categories(self, meal):
        """Extracts meal categories"""
        categories = []
        if meal.get("strCategory"):
            categories.append(meal["strCategory"].lower())
        if meal.get("strArea"):
            categories.append(meal["strArea"].lower())
        return categories

    def _extract_ingredients(self, meal):
        """Extracts meal ingredients"""
        ingredients = []
        for i in range(1, 21):
            ingredient = meal.get(f"strIngredient{i}")
            measure = meal.get(f"strMeasure{i}")

            if ingredient and ingredient.strip():
                measure_text = measure.strip() if measure and measure.strip() else ""
                if measure_text:
                    ingredients.append(f"{measure_text} {ingredient.strip()}")
                else:
                    ingredients.append(ingredient.strip())
        return ingredients
