"""Flask extensions initialization."""
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

# Initialize extensions
db = SQLAlchemy()
cache = Cache()

def init_extensions(app):
    """Initialize Flask extensions"""
    db.init_app(app)
    
    # Configure Flask-Cache
    app.config.setdefault('CACHE_TYPE', 'simple')
    app.config.setdefault('CACHE_DEFAULT_TIMEOUT', 300)
    cache.init_app(app)
