from flask import Flask
from flask_cors import CORS
from config import config
from database.db import Database
from routes.players import players_bp
from routes.teams import teams_bp
from routes.match import match_bp

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app)
    
    # Initialize database
    Database.ensure_files_exist()
    
    # Register blueprints
    app.register_blueprint(players_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(match_bp)
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {"status": "ok"}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
