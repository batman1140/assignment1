"""Seed data for the campaign targeting database."""
from core.models import Campaign, TargetingRule, db

def seed_db():
    """Seed the database with example data from requirements."""
    
    # Create example campaigns
    campaigns = [
        Campaign(
            id="spotify",
            name="Spotify - Music for everyone",
            image="https://somelink",
            cta="Download",
            status="ACTIVE"
        ),
        Campaign(
            id="duolingo",
            name="Duolingo: Best way to learn",
            image="https://somelink2",
            cta="Install",
            status="ACTIVE"
        ),
        Campaign(
            id="subwaysurfer",
            name="Subway Surfer",
            image="https://somelink3",
            cta="Play",
            status="ACTIVE"
        )
    ]
    
    # Add campaigns to session
    for campaign in campaigns:
        db.session.add(campaign)
    
    # Create targeting rules
    rules = [
        TargetingRule(
            campaign_id="spotify",
            include_country="US,Canada"
        ),
        TargetingRule(
            campaign_id="duolingo",
            include_os="android,ios",
            exclude_country="US"
        ),
        TargetingRule(
            campaign_id="subwaysurfer",
            include_os="android",
            include_app="com.gametion.ludokinggame"
        )
    ]
    
    # Add rules to session
    for rule in rules:
        db.session.add(rule)
    
    # Commit all changes
    db.session.commit()

