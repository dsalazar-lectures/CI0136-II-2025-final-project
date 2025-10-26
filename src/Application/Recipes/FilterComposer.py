from src.Application.Recipes.BaseRecipeFilter import BaseRecipeFilter
from src.Application.Recipes.AuthorFilter import AuthorFilter
from src.Application.Recipes.CategoryFilter import CategoryFilter
from src.Application.Recipes.DurationFilter import DurationFilter
from src.Application.Recipes.CalificationFilter import CalificationFilter
from src.Application.Recipes.IngredientsFilter import IngredientsFilter
from src.Application.Recipes.PortionsFilter import PortionsFilter
from src.Application.Recipes.DislikesFilter import DislikesFilter


class FilterComposer:
    """Composes multiple filters using the Decorator pattern to build a filter chain"""
    
    def __init__(self):
        # Map filter names to filter classes
        self.filter_map = {
            'author': AuthorFilter,
            'category': CategoryFilter,
            'duration': DurationFilter,
            'rating': CalificationFilter,
            'ingredients': IngredientsFilter,
            'portions': PortionsFilter,
            'dislikes': DislikesFilter
        }
    
    def apply_filters(self, recipes, filter_criteria):
        """
        Build a decorator chain and apply all filters in a single pass.
        1. Build the chain (BaseFilter -> Filter1 -> Filter2 -> ...)
        2. Apply the entire chain once
        """
        if not filter_criteria:
            return recipes
        
        # Start with base filter (returns all recipes unchanged)
        filter_chain = BaseRecipeFilter()
        
        # Wrap each filter around the previous one
        for filter_name, filter_value in filter_criteria.items():
            if not self._is_valid_value(filter_value):
                continue
                
            filter_class = self.filter_map.get(filter_name)
            if filter_class:
                # Each filter wraps the previous one (Decorator pattern)
                filter_chain = filter_class(filter_chain, filter_value)
        
        return filter_chain.filter(recipes)
    
    def _is_valid_value(self, value):
        return value is not None and value != ''
