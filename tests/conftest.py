"""Test configuration and fixtures."""
import pytest
from app import create_app
from core.models import db
from db.seed import seed_db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('test')
    
    # Create tables and load test data
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_db()  # Load example data from requirements
    
    yield app
    
    # Cleanup after tests
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def seed_data():
    """Example data from the requirements document."""
    return {
        'campaigns': [
            {
                'id': 'spotify',
                'name': 'Spotify - Music for everyone',
                'image': 'https://somelink',
                'cta': 'Download',
                'status': 'ACTIVE'
            },
            {
                'id': 'duolingo',
                'name': 'Duolingo: Best way to learn',
                'image': 'https://somelink2',
                'cta': 'Install',
                'status': 'ACTIVE'
            },
            {
                'id': 'subwaysurfer',
                'name': 'Subway Surfer',
                'image': 'https://somelink3',
                'cta': 'Play',
                'status': 'ACTIVE'
            }
        ],
        'rules': [
            {
                'campaign_id': 'spotify',
                'include_country': 'US,Canada'
            },
            {
                'campaign_id': 'duolingo',
                'include_os': 'android,ios',
                'exclude_country': 'US'
            },
            {
                'campaign_id': 'subwaysurfer',
                'include_os': 'android',
                'include_app': 'com.gametion.ludokinggame'
            }
        ]
    }