"""Initialize MongoDB collections and indexes."""
from flask import current_app
from core.mongodb import mongo

def init_mongodb_collections():
    """Create collections and indexes for MongoDB."""
    with current_app.app_context():
        # Create collections if they don't exist
        db = mongo.db
        
        # Campaigns collection
        if 'campaigns' not in db.list_collection_names():
            db.create_collection('campaigns')
        
        # Create indexes
        db.campaigns.create_index('id', unique=True)
        db.campaigns.create_index('status')
        
        # Targeting rules collection
        if 'targeting_rules' not in db.list_collection_names():
            db.create_collection('targeting_rules')
            
        # Create indexes
        db.targeting_rules.create_index('campaign_id')
        db.targeting_rules.create_index([
            ('include_country', 1),
            ('include_os', 1),
            ('include_app', 1)
        ])
