# Decorator Pattern - Por Mientras

# Description

Decorator is a structural design pattern that allows dynamically overlapping behaviours to a single object by using a special wrapper containing them. This approach allows changes in behaviour at runtime. This works because of the wrapper which is an object that can be linked to a target object as it contains the same set of methods as the target and delegates to it all requests received. 

It’s structure relies on the **Component** which declares the common interface for both wrappers and wrapped objects, the **Concrete Component** which is a class of objects being wrapped and defines the basic behaviour that can be altered by decorators, the **Base Decorator** which contains a field for referencing a wrapped object and delegates all operations to it, and lastly the **Concrete Decorators** which add specific behaviours before or after delegating to the wrapped object. The **Client** can wrap components in multiple layers as long as it works via the component interface.

# Functionality

The Decorator design pattern was used in the filtering of the recipes in order to allow a single filter to be applied or as many filters as the client desires in a single request.

# Motivation

- **Adding filters at runtime** without modifying the original object

- **Open-Closed Principle** as it allows extending object behaviours without altering existing code

- **Working with composition rather than Inheritance** as it would bring a rigid class Hierarchy when combining the different filters

- **Facilitates adding new filters** without touching the already implemented ones

# Implementation explanation

The implementation follows the Decorator pattern with the following components:

### 1. Component Interface (IFilter.py)

```python
class IFilter(ABC):
    @abstractmethod
    def filter(self, criteria):
        pass
```

This defines the model that all filters must follow.

### 2. Concrete Component (BaseRecipeFilter.py)

```python
class BaseRecipeFilter(IFilter):
    def filter(self, recipes):
        return recipes
```

This is the starting point of any filter chain. It implements `IFilter` and simply returns all recipes without any filtering. This works as the foundation that decorators wrap around.

### 3. Base Decorator (RecipeFilter.py)

```python
class RecipeFilter(IFilter):
    def __init__(self, filter_component: IFilter):
        self._filter = filter_component
    
    def filter(self, recipes):
        return self._filter.filter(recipes)
```

This abstract decorator class holds a reference to an `IFilter` component and delegates the filtering operation to it. All concrete decorators inherit from this class.

### 4. Concrete Decorators

Each filter, for example `IngredientsFilter`, `DurationFilter`, `CategoryFilter`, etc... extends `RecipeFilter` and adds its specific filtering logic:

- **IngredientsFilter:** Filters recipes containing specified ingredients
- **DurationFilter:** Filters recipes by maximum cooking duration
- **PortionsFilter:** Filters recipes within a portion range (e.g., "2-4")
- **CategoryFilter:** Filters recipes by category tags
- **AuthorFilter:** Filters recipes by author name
- **CalificationFilter:** Filters recipes by minimum rating
- **DislikesFilter:** Excludes recipes containing unwanted ingredients

Each decorator calls the wrapped filter method, applies its own filtering logic to the results and returns the filtered list.

### Filter Composition with `FilterComposer`

The `FilterComposer` class manages the creation of the decorator chain:

```python
class FilterComposer:
    def apply_filters(self, recipes, filter_criteria):
        # Start with base filter
        filter_chain = BaseRecipeFilter()
        
        # Wrap each filter around the previous one
        for filter_name, filter_value in filter_criteria.items():
            if self._is_valid_value(filter_value):
                filter_class = self.filter_map.get(filter_name)
                if filter_class:
                    filter_chain = filter_class(filter_chain, filter_value)
        
        return filter_chain.filter(recipes)
```

The implementation keeps a `filter_map` dictionary mapping filters to their classes, then builds the chain by progressively wrapping each decorator around the previous one. After that, it validates filter values before applying them. Finally, executes the entire chain with a single call to `filter()`.

#### Example chain:

```python
DislikesFilter -> IngredientsFilter -> DurationFilter -> BaseRecipeFilter
```
### Integration with the Service Layer

The `recipe_service.py` uses the FilterComposer to provide filtering functionality:

```python
def filter_recipes(filter_criteria):
    all_recipes = recipe_repository.get_all()
    return filter_composer.apply_filters(all_recipes, filter_criteria)
```

This allows the application layer to pass filter criteria and receive filtered results without knowing the internal decorator implementation.

### Adding new filters

To add a new filter:

1. Create a new concrete decorator inheriting from `RecipeFilter`
2. Implement the filtering logic in the `filter()` method
4. Register it in `FilterComposer.filter_map`


# References

https://www.geeksforgeeks.org/system-design/decorator-pattern/

https://refactoring.guru/design-patterns/decorator