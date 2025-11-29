from abc import ABC, abstractmethod
from typing import Optional
from src.Model.Ingredients.Ingredients import Ingredient


class IExternalIngredientProvider(ABC):
    """
    Define el contrato (Interfaz) que cualquier proveedor de datos
    de ingredientes externos debe implementar.

    Esto asegura que la capa Application (IngredientUseCase) no dependa de
    detalles de infraestructura como Spoonacular.
    """

    @abstractmethod
    def search_ingredient(self, name: str) -> Optional[Ingredient]:
        """
        Busca un ingrediente por nombre en la fuente externa.

        El método debe devolver una instancia de nuestro modelo Ingredient
        o None si no se encuentra.
        """
        pass
