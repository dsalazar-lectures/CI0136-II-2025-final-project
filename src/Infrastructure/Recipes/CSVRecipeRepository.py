import csv
from src.Database.Recipes.RecipesSchema import system_recipes, PATH
from src.Model.Recipes.Recipes import Recipe
from src.Application.Recipes.IRecipeRepository import IRecipeRepository

# storage for user-created recipes separate from CSV system_recipes
user_recipes = []


class CSVRecipeRepository(IRecipeRepository):
    def get_all(self):
        return system_recipes + user_recipes

    def get_by_id(self, recipe_id):
        return next(
            (recipe for recipe in system_recipes if recipe.id == recipe_id), None
        )

    def find_by_ingredient(self, ingredient):
        ingredient = ingredient.lower()
        return [
            recipe
            for recipe in system_recipes
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
                    ]
                )

    def add_recipe(self, recipe_data):
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
