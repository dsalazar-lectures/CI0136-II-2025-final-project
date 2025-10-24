from flask import Flask
from src.API.AuthRoutes import auth_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.route('/')
    def health_check():
        return {
            "status": "API is running",
            "endpoints": [ "POST /auth/register",
                "POST /auth/login",
                "PUT /auth/change-username",
                "GET /ingredients",
                "GET /recipes"
            ]
               
        }

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)