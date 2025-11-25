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
# No levantar excepción en import; permitir que la app/tests funcionen sin clave.
api_service = None
spoonacular_adapter = None

if API_KEY_SPOONACULAR:
    api_service = SpoonacularAPIService(api_key=API_KEY_SPOONACULAR)
    spoonacular_adapter = SpoonacularIngredientAdapter(api_service=api_service)
else:
    # Mensaje informativo (no obligatorio)
    print("WARNING: SPOONACULAR_API_KEY no definida - proveedor externo deshabilitado.")

ingredient_repository = IngredientRepository()

ingredient_service_instance = IngredientUseCase(
    repository=ingredient_repository, external_provider=spoonacular_adapter
)
