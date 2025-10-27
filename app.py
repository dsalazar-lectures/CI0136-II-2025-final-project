from flask import Flask
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Import blueprints
from src.API.Ingredients.IngredientsRoutes import ingredients_bp
from src.API.Recipes.recipesRoutes import recipes_bp
from src.API.Menu.menuRoutes import recipes_bp as menu_bp
from src.API.AuthRoutes import auth_bp

from src.API.Metrics.DashboardRoute import dashboard_bp

def create_app():
    app = Flask(__name__)

    app.json.ensure_ascii = False

    # Register blueprints
    app.register_blueprint(ingredients_bp)
    app.register_blueprint(recipes_bp, url_prefix="/api")
    app.register_blueprint(menu_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix='/api')

    # Health check endpoint
    @app.route("/")
    def health_check():
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
                "GET /api/Services/metrics/open-dashboard?port=8601",
            ],
        }

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
