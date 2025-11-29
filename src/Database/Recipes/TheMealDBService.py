import requests

class TheMealDBService:
    
    def __init__(self):
        self.base_url = "https://www.themealdb.com/api/json/v1/1"
    
    def obtain_recipes(self, query=""):
        url = f"{self.base_url}/search.php?s={query}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("meals", [])
        except requests.exceptions.RequestException:
            return []