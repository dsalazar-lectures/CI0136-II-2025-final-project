from dotenv import load_dotenv
import os
from src.Infrastructure.Ingredients.IngredientRepository import IngredientRepository
from src.Infrastructure.Ingredients.external.SpoonacularAPIService import (
    SpoonacularAPIService,
)
from src.Infrastructure.Ingredients.external.SpoonacularIngredientAdapter import (
    SpoonacularIngredientAdapter,
)
from src.Infrastructure.Ingredients.external.FoodDataAPIService import (
    FoodDataAPIService,
)
from src.Infrastructure.Ingredients.external.FoodDataIngredientAdapter import (
    FoodDataIngredientAdapter,
)
from .IngredientUseCase import IngredientUseCase

load_dotenv()

API_KEY_SPOONACULAR = os.getenv("SPOONACULAR_API_KEY")
API_KEY_FOODDATA = os.getenv("FOODDATA_API_KEY")

spoonacular_service = None
spoonacular_adapter = None
fooddata_api_service = None
fooddata_adapter = None

if API_KEY_SPOONACULAR:
    spoonacular_service = SpoonacularAPIService(api_key=API_KEY_SPOONACULAR)
    spoonacular_adapter = SpoonacularIngredientAdapter(api_service=spoonacular_service)
else:
    print("WARNING: SPOONACULAR_API_KEY no definida - proveedor externo deshabilitado.")

if API_KEY_FOODDATA:
    fooddata_api_service = FoodDataAPIService(api_key=API_KEY_FOODDATA)
    fooddata_adapter = FoodDataIngredientAdapter(api_service=fooddata_api_service)
else:
    print("WARNING: FOODDATA_API_KEY no definida - proveedor externo deshabilitado.")

ingredient_repository = IngredientRepository()

ingredient_service_instance = IngredientUseCase(
    repository=ingredient_repository,
    external_providers=[spoonacular_adapter, fooddata_adapter],
)
