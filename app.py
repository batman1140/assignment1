from flask import Flask
from api.delivery import delivery_bp
from config.config import get_config
from core.extensions import db
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import os

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV') or 'dev'
    app = Flask(__name__)
    app.config.from_object(get_config())
      # Initialize SQLAlchemy
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(delivery_bp)
    
    # Add Prometheus metrics endpoint
    app.wsgi_app = DispatcherMiddleware(
        app.wsgi_app, 
        {'/metrics': make_wsgi_app()}
    )
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Initialize and seed database
    with app.app_context():
        from db.seed import seed_db
        seed_db()
    
    app.run(debug=True)