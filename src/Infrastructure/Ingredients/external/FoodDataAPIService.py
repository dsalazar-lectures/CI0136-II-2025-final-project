import requests
from typing import Optional, Dict

BASE_URL = "https://api.nal.usda.gov/fdc/v1"


class FoodDataAPIService:
    """Class to interact with USDA FoodData Central API for ingredient data."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_ingredient_data(self, name: str) -> Optional[Dict]:
        """
        Search for ingredients by name and return raw JSON from the API.
        """

        search_endpoint = "/foods/search"
        url = BASE_URL + search_endpoint

        params = {"api_key": self.api_key, "query": name, "pageSize": 1}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            foods = data.get("foods")
            if not foods:
                return None

            # Get detailed information for the first result
            fdc_id = foods[0].get("fdcId")
            if not fdc_id:
                return None

            info_endpoint = f"/food/{fdc_id}"
            info_url = BASE_URL + info_endpoint

            info_params = {"api_key": self.api_key}

            info_response = requests.get(info_url, params=info_params, timeout=10)
            info_response.raise_for_status()

            return info_response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error en la API de USDA FoodData Central: {e}")
            return None
        except Exception as e:
            print(f"Error procesando datos de USDA FoodData Central: {e}")
            return None
