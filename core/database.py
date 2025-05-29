"""Database extension initialization."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initialize database."""
    db.init_app(app)
