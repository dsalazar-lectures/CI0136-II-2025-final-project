from abc import ABC, abstractmethod

class IMenuRepository(ABC):
    
    @abstractmethod
    def generate_menus(self, recipes, count):
        pass