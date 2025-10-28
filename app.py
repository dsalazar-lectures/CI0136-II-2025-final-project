from flask import Flask
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Import blueprints
from src.API.Ingredients.IngredientsRoutes import ingredients_bp
from src.API.Recipes.recipesRoutes import recipes_bp
from src.API.Menu.menuRoutes import menu_bp
from src.API.AuthRoutes import auth_bp

from src.API.Metrics.DashboardRoute import dashboard_bp
from src.API.Profiles.ProfileRoutes import profiles_bp


def create_app():
    app = Flask(__name__)

    app.json.ensure_ascii = False

    # Register blueprints
    app.register_blueprint(ingredients_bp, url_prefix='/api')
    app.register_blueprint(recipes_bp, url_prefix='/api')
    app.register_blueprint(menu_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(profiles_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api")

    # Health check endpoint
    @app.route("/")
    def health_check():
        return {"status": "API is running", "endpoints": [
            "GET /api/ingredients - Get all ingredients",
            "GET /api/ingredients/<id> - Get ingredient by ID",
            "POST /api/ingredients/search - Search ingredient(s) by name, "
            "category or id",
            "GET /api/recipes - Get all recipes",
            "GET /api/recipes/<id> - Get recipe by ID"
        ]}
    
        return {
            "status": "API is running",
            "endpoints": [
                "POST /auth/register",
                "POST /auth/login",
                "GET /api/ingredients - Get all ingredients",
                "GET /api/ingredients/<id> - Get ingredient by ID",
                "GET /api/recipes - Get all recipes",
                "GET /api/recipes/<id> - Get recipe by ID",
                "GET /api/menu?category=<category> - Get all menu items",
                "GET /api/menu/email - Email selected recipies to specific address",
                "GET /api/Services/metrics/open-dashboard?port=8601",
                "GET /api/profiles/<user_id>/favorite-menus - Get user's favorite menus",
                "POST /api/profiles/<user_id>/favorite-menus - Add menu to favorites",
                "DELETE /api/profiles/<user_id>/favorite-menus/<menu_id> - Remove menu from favorites",
            ],
        }

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
