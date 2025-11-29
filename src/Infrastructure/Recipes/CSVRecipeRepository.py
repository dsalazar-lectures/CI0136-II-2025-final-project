import csv
from src.Database.Recipes.RecipesSchema import system_recipes, PATH, load_recipes
from src.Model.Recipes.Recipes import Recipe
from src.Application.Recipes.IRecipeRepository import IRecipeRepository
from src.Database.Recipes.APIRecipesSchema import api_recipes, load_api_recipes

# storage for user-created recipes separate from CSV system_recipes


class CSVRecipeRepository(IRecipeRepository):
    def get_all(self):
        load_recipes()
        load_api_recipes()
        all_recipes = system_recipes + api_recipes
        return all_recipes

    def get_api_recipes():
        load_api_recipes()
        return api_recipes

    def get_system_recipes():
        load_recipes()
        return system_recipes

    def get_by_id(self, recipe_id):
        load_recipes()
        load_api_recipes()
        all_recipes = system_recipes + api_recipes
        return next((recipe for recipe in all_recipes if recipe.id == recipe_id), None)

    def find_by_ingredient(self, ingredient):
        load_recipes()
        load_api_recipes()
        all_recipes = system_recipes + api_recipes
        ingredient = ingredient.lower()
        return [
            recipe
            for recipe in all_recipes
            if any(ingredient in ing.lower() for ing in recipe.ingredients)
        ]

    def build_recipe(self, data):
        return Recipe(
            data["id"],
            data["name"],
            str(data["categories"]),
            str(data["ingredients"]),
            data["duration"],
            data["instructions"],
            data["portions"],
            data["author"],
            0,
            0,
            0,
            "[]",
        )

    def save_to_csv(self, recipe):
        with open(PATH, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    recipe.id,
                    recipe.name,
                    recipe.categories,
                    recipe.ingredients,
                    recipe.duration,
                    recipe.instructions,
                    recipe.portions,
                    recipe.author,
                    recipe.califications_sumatory,
                    recipe.califications_amount,
                    recipe.users_used_recipe,
                    recipe.users_rated,
                ]
            )

    def rewrite_csv(self):
        # Overwrite the recipes CSV with the current in-memory system_recipes
        header = [
            "id",
            "name",
            "categories",
            "ingredients",
            "duration",
            "instructions",
            "portions",
            "author",
            "calificationsSumatory",
            "calificationsAmount",
            "usersUsedRecipe",
            "usersRated",
        ]
        with open(PATH, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for r in system_recipes:
                writer.writerow(
                    [
                        r.id,
                        r.name,
                        r.categories,
                        r.ingredients,
                        r.duration,
                        r.instructions,
                        r.portions,
                        r.author,
                        r.califications_sumatory,
                        r.califications_amount,
                        r.users_used_recipe,
                        r.users_rated,
                    ]
                )

    def add_recipe(self, recipe_data):
        load_recipes()
        recipe_data["id"] = max((recipe.id for recipe in system_recipes), default=0) + 1
        recipe = self.build_recipe(recipe_data)
        system_recipes.append(recipe)
        self.save_to_csv(recipe)
        return recipe

    def delete_if_owned(self, recipe_id, username):
        # Delete only if recipe exists in system_recipes and is owned by username
        recipe = self.get_by_id(recipe_id)
        if recipe is None:
            return None
        if recipe.author != username:
            return False
        system_recipes.remove(recipe)
        self.rewrite_csv()
        return recipe

    def update_if_owned(self, recipe_id, username, updates: dict):
        recipe = self.get_by_id(recipe_id)
        if recipe is None:
            return None
        if recipe.author != username:
            return False

        allowed = {
            "name": str,
            "categories": list,
            "ingredients": list,
            "duration": int,
            "instructions": str,
            "portions": int,
        }
        for field, caster in allowed.items():
            if field in updates and updates[field] is not None:
                value = updates[field]
                value = list(value) if caster is list else caster(value)
                setattr(recipe, field, value)

        self.rewrite_csv()
        return recipe

    def find_by_category(self, category):
        load_recipes()
        load_api_recipes()
        all_recipes = api_recipes + system_recipes
        category = category.lower()
        return [
            recipe
            for recipe in all_recipes
            if any(
                category in str(recipe_category).lower()
                for recipe_category in (recipe.categories)
            )
        ]

    def rate_recipe(self, recipe_id, username, rating):
        load_recipes()
        recipe = self.get_by_id(recipe_id)

        if recipe is None:
            return None

        if username in recipe.users_rated:
            return False

        recipe.califications_sumatory += rating
        recipe.califications_amount += 1
        recipe.users_rated.append(username)

        self.rewrite_csv()
        return recipe

    def find_by_categories(self, categories):
        load_recipes()

        if categories is None:
            return []

        if isinstance(categories, str):
            categories = [c.strip() for c in categories.split(",") if c.strip()]

        search_terms = [str(c).lower() for c in categories]

        result = []
        for recipe in system_recipes:
            recipe_categories = [str(rc).lower() for rc in recipe.categories]
            if any(term in recipe_categories for term in search_terms):
                result.append(recipe)

        return result
