from flask import Flask
from dotenv import load_dotenv
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Import blueprints
from src.API.Ingredients.IngredientsRoutes import ingredients_bp
from src.API.Recipes.recipesRoutes import recipes_bp
from src.API.Menu.menuRoutes import menu_bp
from src.API.AuthRoutes import auth_bp, google_bp
from src.API.Profiles.ProfileRoutes import profiles_bp

from src.API.Metrics.DashboardRoute import dashboard_bp


def create_app():
    app = Flask(__name__)

    app.json.ensure_ascii = False

    # Secret key for sessions with Google
    load_dotenv()
    app.secret_key = os.getenv("SECRET_KEY", "dev-dafult-key")

    # Register blueprints
    app.register_blueprint(ingredients_bp)
    app.register_blueprint(recipes_bp, url_prefix="/api")
    app.register_blueprint(menu_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(google_bp, url_prefix="/auth")
    app.register_blueprint(profiles_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api")

    # Health check endpoint
    @app.route("/")
    def health_check():
        return {
            "status": "API is running",
            "endpoints": [
                "POST /auth/register",
                "POST /auth/login",
                "GET /auth/login-google",
                "POST /auth/regenerate-key",
                "POST /auth/change-password",
                "GET /api/ingredients - Get all ingredients",
                "GET /api/ingredients/<id> - Get ingredient by ID",
                "GET /api/recipes - Get all recipes",
                "GET /api/recipes/<id> - Get recipe by ID",
                "GET /api/menu?category=<category> - Get all menu items",
                "GET /api/menu/email - Email selected recipies to specific address",
                "GET /api/menu/customized?user_id=<id>&category=<cat-optional> - GET all recipes based in favorite ingredients",
                "GET /api/profiles/<user_id> - GET profile by user ID",
                "PUT /api/profiles/<user_id>/favorites - PUT user ID and favorite ingredients",
                "GET /api/profiles/<user_id>/favorite-menus - Get user's favorite menus",
                "POST /api/profiles/<user_id>/favorite-menus - Add menu to favorites",
                "DELETE /api/profiles/<user_id>/favorite-menus - Remove menu from favorites",
                "GET /api/menu/<category>/<count> - Generate N menus for a category",
                "GET /api/Services/metrics/open-dashboard?port=8601",
            ],
        }

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
