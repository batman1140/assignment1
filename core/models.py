"""Database models for the targeting engine."""
from datetime import datetime
from .extensions import db

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(1024), nullable=False)
    cta = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # ACTIVE or INACTIVE
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    targeting_rules = db.relationship('TargetingRule', backref='campaign', lazy=True)

    @classmethod
    def create(cls, id, name, image, cta, status):
        campaign = {
            "id": id,
            "name": name,
            "image": image,
            "cta": cta,
            "status": status,
            "created_at": datetime.utcnow()
        }
        cls().collection.insert_one(campaign)
        return campaign

    @classmethod
    def get_active_campaigns(cls):
        return cls().collection.find({"status": "ACTIVE"})
    
    @classmethod
    def get_by_id(cls, id):
        return cls().collection.find_one({"id": id})

    def to_dict(self):
        """Convert campaign to API response format"""
        return {
            "cid": self["id"],
            "img": self["image"],
            "cta": self["cta"]
        }

class TargetingRule:
    @property
    def collection(self):
        return get_db().targeting_rules

    @classmethod
    def create(cls, campaign_id, include_country=None, exclude_country=None,
              include_os=None, exclude_os=None, include_app=None, exclude_app=None):
        rule = {
            "campaign_id": campaign_id,
            "include_country": include_country,
            "exclude_country": exclude_country,
            "include_os": include_os,
            "exclude_os": exclude_os,
            "include_app": include_app,
            "exclude_app": exclude_app,
            "created_at": datetime.utcnow()
        }
        cls().collection.insert_one(rule)
        return rule

    @classmethod
    def get_by_campaign(cls, campaign_id):
        return cls().collection.find({"campaign_id": campaign_id})

    @staticmethod
    def matches(rule, app_id: str, country: str, os: str) -> bool:
        """Check if a request matches this targeting rule"""
        
        # Check inclusion rules
        if rule.get('include_country') and country not in rule['include_country'].split(','):
            return False
        if rule.get('include_os') and os not in rule['include_os'].split(','):
            return False
        if rule.get('include_app') and app_id not in rule['include_app'].split(','):
            return False
            
        # Check exclusion rules
        if rule.get('exclude_country') and country in rule['exclude_country'].split(','):
            return False
        if rule.get('exclude_os') and os in rule['exclude_os'].split(','):
            return False
        if rule.get('exclude_app') and app_id in rule['exclude_app'].split(','):
            return False
            
        return True