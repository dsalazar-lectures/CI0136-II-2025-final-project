# Adapter Pattern - Por Mientras

# Description

Adapter is a structural design pattern that allows objects with incompatible interfaces to collaborate. It acts as a bridge between two incompatible interfaces by wrapping an existing class with a new interface that clients expect. The adapter converts the interface of a class into another interface that clients can work with, enabling classes to work together that couldn't otherwise due to incompatible interfaces.

Its structure relies on the **Target Interface** which defines the domain-specific interface that the client uses, the **Adaptee** which is an existing class with an incompatible interface that needs adapting, the **Adapter** which implements the target interface and wraps the adaptee to make it compatible, and the **Client** which works with objects through the target interface without knowing about the adapter implementation details.

# Functionality

The Adapter design pattern was used to integrate TheMealDB API as an external recipe source into the application. It allows the system to consume recipes from TheMealDB while maintaining a consistent internal recipe format, enabling seamless integration of external data sources without modifying the core application logic.

# Motivation

- **Integrating external APIs** without coupling the system to specific API structures

- **Single Responsibility Principle** as it separates data conversion logic from core business logic

- **Open-Closed Principle** as new external sources can be added without modifying existing code

- **Reusability** as the same adapter pattern can be used for different external recipe sources

- **Flexibility** in switching or adding multiple external data sources at runtime

# Implementation explanation

The implementation follows the Adapter pattern with the following components:

### 1. Target Interface (IExternalRecipeSource.py)
```python
class IExternalRecipeSource(ABC):
    @abstractmethod
    def get_raw_data(self):
        pass
    
    @abstractmethod
    def parse_recipe(self, raw_data):
        pass
```

This defines the interface that the application expects all external recipe sources to implement, providing a consistent contract for obtaining and parsing recipe data.

### 2. Adaptee (TheMealDBService.py)
```python
class TheMealDBService:
    def __init__(self):
        self.base_url = "https://www.themealdb.com/api/json/v1/1"
    
    def obtain_recipes(self, query=""):
        url = f"{self.base_url}/search.php?s={query}"
        response = requests.get(url)
        data = response.json()
        return data.get("meals", [])
```

This is the existing service that communicates directly with TheMealDB API. It has its own interface that is incompatible with what the application expects, returning raw API data in TheMealDB's specific format.

### 3. Adapter (TheMealDBAdapter.py)
```python
class TheMealDBAdapter(IExternalRecipeSource):
    def __init__(self):
        self.service = TheMealDBService()
    
    def get_raw_data(self):
        return self.service.obtain_recipes("")
    
    def parse_recipe(self, meal):
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
```

The adapter implements `IExternalRecipeSource` and wraps `TheMealDBService`. It translates TheMealDB's API response format into the application's internal recipe format through the following adaptations:

- **Field Mapping:** Converts API fields (e.g., `strMeal`, `idMeal`) to application fields (e.g., `name`, `id`)
- **Data Extraction:** Extracts and processes categories from `strCategory` and `strArea` fields
- **Ingredient Processing:** Iterates through 20 possible ingredient/measure pairs and formats them consistently
- **Default Values:** Provides default values for fields not present in the API (e.g., `duration`, rating fields)

### 4. Client Integration (APIRecipesSchema.py)
```python
def load_api_recipes():
    global api_recipes
    api_recipes.clear()
    
    adapter = TheMealDBAdapter()
    meals = adapter.get_raw_data()
    
    if meals:
        parsed_recipes = [adapter.parse_recipe(meal) for meal in meals]
        write_api_recipes(parsed_recipes)
```

The client code uses the adapter through the `IExternalRecipeSource` interface, remaining unaware of TheMealDB's specific implementation details. It simply requests raw data and parses it using the standardized interface.

### Data Transformation Process

The adapter performs several key transformations:

1. **Categories Extraction:** Combines `strCategory` and `strArea` into a unified categories list
2. **Ingredients Formatting:** Consolidates up to 20 ingredient-measure pairs into clean formatted strings
3. **Field Normalization:** Maps TheMealDB's naming convention to the application's schema
4. **Type Conversion:** Converts lists to string representations for CSV storage compatibility

### Adding new external sources

To add a new external recipe source:

1. Create a new service class to communicate with the external API
2. Create a new adapter class implementing `IExternalRecipeSource`
3. Implement `get_raw_data()` to fetch from the new source
4. Implement `parse_recipe()` to transform the source's format to the application's format
5. Use the adapter in `APIRecipesSchema.py` or wherever external recipes are loaded

# References

https://www.geeksforgeeks.org/adapter-pattern/

https://refactoring.guru/design-patterns/adapter