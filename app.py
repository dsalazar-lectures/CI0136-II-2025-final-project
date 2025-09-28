from flask import Flask
from src.API.Recipes.recipesRoutes import recipes_bp
from src.Database.Recipes.RecipesSchema import load_recipes

app = Flask(__name__)
app.register_blueprint(recipes_bp)

if __name__ == "__main__":
    load_recipes()
    app.run(debug=True)