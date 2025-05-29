"""Database models for the targeting engine."""
from .extensions import db

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(1024), nullable=False)
    cta = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # ACTIVE or INACTIVE

    def __repr__(self):
        return f"<Campaign {self.id}>"
    def to_dict(self):
        """Convert campaign to API response format"""
        return {
            "cid": self.id,
            "img": self.image,
            "cta": self.cta
        }

class TargetingRule(db.Model):
    __tablename__ = 'targeting_rules'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.String(255), db.ForeignKey('campaigns.id'), nullable=False)
    include_country = db.Column(db.String(1024))
    exclude_country = db.Column(db.String(1024))
    include_os = db.Column(db.String(1024))
    exclude_os = db.Column(db.String(1024))
    include_app = db.Column(db.String(1024))
    exclude_app = db.Column(db.String(1024))

    campaign = db.relationship("Campaign", backref=db.backref("targeting_rules", lazy=True))

    def __repr__(self):
        return f"<TargetingRule {self.id} for Campaign {self.campaign_id}>"
    def matches(self, app_id: str, country: str, os: str) -> bool:
        """Check if a request matches this targeting rule"""
        
        # Check inclusion rules
        if self.include_country and country not in self.include_country.split(','):
            return False
        if self.include_os and os not in self.include_os.split(','):
            return False
        if self.include_app and app_id not in self.include_app.split(','):
            return False
            
        # Check exclusion rules
        if self.exclude_country and country in self.exclude_country.split(','):
            return False
        if self.exclude_os and os in self.exclude_os.split(','):
            return False
        if self.exclude_app and app_id in self.exclude_app.split(','):
            return False
            
        return True