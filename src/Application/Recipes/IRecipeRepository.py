import csv
from src.Database.Recipes.RecipesSchema import system_recipes, PATH
from src.Model.Recipes.Recipes import Recipe

class RecipeRepository:
    def get_all(self):
        return system_recipes

    def get_by_id(self, recipe_id):
        return next((recipe for recipe in system_recipes if recipe.id == recipe_id), None)
    
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
            0
        )
    
    def save_to_csv(self, recipe):
        with open(PATH, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
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
                recipe.users_used_recipe
            ])
    
    def add_recipe(self, recipe_data):
        recipe_data["id"] = max((recipe.id for recipe in system_recipes), default=0) + 1
        recipe = self.build_recipe(recipe_data)
        system_recipes.append(recipe)
        self.save_to_csv(recipe)
        return recipe

recipe_repository = RecipeRepository()
