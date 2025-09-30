from flask import Flask
import sys
import os

# Add src directory to path for imports  
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import blueprints
from src.API.Ingredients.IngredientsRoutes import ingredients_bp
from src.API.Recipes.recipesRoutes import recipes_bp

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(ingredients_bp, url_prefix='/api')
    app.register_blueprint(recipes_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/')
    def health_check():
        return {"status": "API is running", "endpoints": [
            "GET /api/ingredients - Get all ingredients",
            "GET /api/ingredients/<id> - Get ingredient by ID", 
            "GET /api/recipes - Get all recipes",
            "GET /api/recipes/<id> - Get recipe by ID"
        ]}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)