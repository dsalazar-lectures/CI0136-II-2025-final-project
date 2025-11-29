from abc import ABC, abstractmethod

class IExternalRecipeSource(ABC):
    
    @abstractmethod
    def get_raw_data(self):
        """Gets raw recipes from external source"""
        pass
    
    @abstractmethod
    def parse_recipe(self, raw_data):
        """Parses data to system recipe format"""
        pass