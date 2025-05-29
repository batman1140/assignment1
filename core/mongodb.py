"""MongoDB connection and utilities."""
from flask_pymongo import PyMongo

# Initialize PyMongo without app context
mongo = PyMongo()

def get_db():
    """Get the MongoDB database instance"""
    return mongo.db

def init_mongodb(app):
    """Initialize MongoDB with the Flask app"""
    # Configure MongoDB
    app.config["MONGO_URI"] = app.config.get('MONGO_URI')
    
    # Initialize MongoDB
    mongo.init_app(app)
    
    # Initialize collections and indexes
    with app.app_context():
        db = mongo.db
        
        # Ensure collections exist
        if 'campaigns' not in db.list_collection_names():
            db.create_collection('campaigns')
        if 'targeting_rules' not in db.list_collection_names():
            db.create_collection('targeting_rules')
            
        # Create indexes
        db.campaigns.create_index('id', unique=True)
        db.campaigns.create_index('status')
        db.targeting_rules.create_index('campaign_id')
        db.targeting_rules.create_index([
            ('include_country', 1),
            ('include_os', 1),
            ('include_app', 1)
        ])
