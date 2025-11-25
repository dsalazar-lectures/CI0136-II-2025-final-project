import requests
from typing import Optional, Dict

BASE_URL = "https://api.spoonacular.com"


class SpoonacularAPIService:
    """Cliente para interactuar directamente con la API de Spoonacular."""

    # ⭐️ CORRECCIÓN: Ahora el constructor SÓLO acepta la clave.
    # Esto obliga a que la clave sea inyectada por el IngredientInjector.
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_ingredient_data(self, name: str) -> Optional[Dict]:
        """
        Busca un ingrediente por nombre y devuelve el JSON crudo de la API.
        Devuelve None si hay error o no se encuentra.
        """

        # El resto del código es correcto y usa self.api_key correctamente.
        search_endpoint = "/food/ingredients/search"
        url = BASE_URL + search_endpoint

        params = {"apiKey": self.api_key, "query": name, "number": 1}

        try:
            # 1. Realizar la búsqueda inicial para obtener el ID
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if not data.get("results"):
                return None

            ingredient_id = data["results"][0]["id"]

            # 2. Obtener la información detallada usando el ID
            info_endpoint = f"/food/ingredients/{ingredient_id}/information"
            info_url = BASE_URL + info_endpoint

            info_params = {"apiKey": self.api_key, "amount": 1, "unit": "portion"}

            info_response = requests.get(info_url, params=info_params)
            info_response.raise_for_status()

            return info_response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error en la API de Spoonacular: {e}")
            return None
        except Exception as e:
            print(f"Error procesando datos de Spoonacular: {e}")
            return None
