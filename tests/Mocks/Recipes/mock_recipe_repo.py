class MockRecipeRepo:
    """Simple dummy repository exposing find_by_category used by tests."""

    def __init__(self, recipes=None):
        self._recipes = recipes or []

    def find_by_category(self, category):
        return [r for r in self._recipes if category in r.categories]
