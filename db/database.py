"""Database initialization and utilities."""
from core.extensions import db

def init_db(app):
    """Initialize the database with the Flask app"""
    db.init_app(app)
    
    # Import models here to avoid circular imports
    from core.models import Campaign, TargetingRule  # noqa: F401
    with app.app_context():
        db.create_all()

def reset_db(app):
    """Reset the database (useful for testing)"""
    db.init_app(app)  # Make sure db is initialized with the current app
    with app.app_context():
        db.drop_all()
        db.create_all()