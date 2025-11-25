from dotenv import load_dotenv
import os
from src.Infrastructure.Ingredients.IngredientRepository import IngredientRepository
from src.Infrastructure.Ingredients.external.SpoonacularAPIService import (
    SpoonacularAPIService,
)
from src.Infrastructure.Ingredients.external.SpoonacularIngredientAdapter import (
    SpoonacularIngredientAdapter,
)
from .IngredientUseCase import IngredientUseCase

load_dotenv()

API_KEY_SPOONACULAR = os.getenv("SPOONACULAR_API_KEY")
if not API_KEY_SPOONACULAR:
    raise RuntimeError("SPOONACULAR_API_KEY no está definida. Añádela en .env")

api_service = SpoonacularAPIService(api_key=API_KEY_SPOONACULAR)

ingredient_repository = IngredientRepository()

spoonacular_adapter = SpoonacularIngredientAdapter(api_service=api_service)

ingredient_service_instance = IngredientUseCase(
    repository=ingredient_repository, external_provider=spoonacular_adapter
)
