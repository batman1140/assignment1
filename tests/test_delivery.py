"""Tests for the campaign delivery service."""

def test_delivery_missing_params(client):
    """Test delivery endpoint with missing parameters."""
    # Test missing app
    response = client.get('/api/v1/delivery?country=germany&os=android')
    assert response.status_code == 400
    assert response.json == {'error': 'missing app param'}

    # Test missing country
    response = client.get('/api/v1/delivery?app=test.app&os=android')
    assert response.status_code == 400
    assert response.json == {'error': 'missing country param'}

    # Test missing os
    response = client.get('/api/v1/delivery?app=test.app&country=germany')
    assert response.status_code == 400
    assert response.json == {'error': 'missing os param'}

def test_delivery_no_matching_campaigns(client):
    """Test when no campaigns match the criteria."""
    response = client.get('/api/v1/delivery?app=com.nonexistent.app&country=fr&os=web')
    assert response.status_code == 204
    assert response.data == b''  # Empty response for no matches

def test_delivery_single_match_spotify(client):
    """Test Spotify campaign targeting for US users."""
    response = client.get('/api/v1/delivery?app=com.anyapp&country=us&os=web')
    assert response.status_code == 200
    data = response.json
    assert len(data) == 1
    assert data[0] == {
        'cid': 'spotify',
        'img': 'https://somelink',
        'cta': 'Download'
    }

def test_delivery_multiple_matches(client):
    """Test case when multiple campaigns match (US/Ludo King/Android)."""
    response = client.get(
        '/api/v1/delivery?app=com.gametion.ludokinggame&country=us&os=android'
    )
    assert response.status_code == 200
    data = response.json
    assert len(data) == 2
    assert {campaign['cid'] for campaign in data} == {'spotify', 'subwaysurfer'}

def test_delivery_include_os(client):
    """Test OS-based targeting (Duolingo: Android/iOS only)."""
    # Should match: Android request
    response = client.get('/api/v1/delivery?app=com.anyapp&country=de&os=android')
    assert response.status_code == 200
    assert any(c['cid'] == 'duolingo' for c in response.json)

    # Should not match: Web request
    response = client.get('/api/v1/delivery?app=com.anyapp&country=de&os=web')
    assert response.status_code == 204

def test_delivery_exclude_country(client):
    """Test country exclusion (Duolingo: exclude US)."""
    # Should match: Germany
    response = client.get('/api/v1/delivery?app=com.anyapp&country=de&os=android')
    assert response.status_code == 200
    assert any(c['cid'] == 'duolingo' for c in response.json)

    # Should not match: US
    response = client.get('/api/v1/delivery?app=com.anyapp&country=us&os=android')
    data = response.json
    assert not any(c['cid'] == 'duolingo' for c in data)

def test_delivery_app_targeting(client):
    """Test app-specific targeting (Subway Surfer: Ludo King only)."""
    # Should match: Ludo King app
    response = client.get(
        '/api/v1/delivery?app=com.gametion.ludokinggame&country=in&os=android'
    )
    assert response.status_code == 200
    assert any(c['cid'] == 'subwaysurfer' for c in response.json)

    # Should not match: Different app
    response = client.get(
        '/api/v1/delivery?app=com.other.app&country=in&os=android'
    )
    data = response.json if response.status_code == 200 else []
    assert not any(c['cid'] == 'subwaysurfer' for c in data)

def test_delivery_case_insensitive(client):
    """Test that country and OS matching is case-insensitive."""
    # Test with mixed case country
    response = client.get('/api/v1/delivery?app=com.anyapp&country=Us&os=android')
    assert response.status_code == 200
    assert any(c['cid'] == 'spotify' for c in response.json)

    # Test with uppercase OS
    response = client.get('/api/v1/delivery?app=com.anyapp&country=de&os=ANDROID')
    assert response.status_code == 200
    assert any(c['cid'] == 'duolingo' for c in response.json)

def test_delivery_inactive_campaign(client, app):
    """Test that inactive campaigns are not returned."""
    from core.models import Campaign, db
    
    # Set Spotify campaign to inactive
    with app.app_context():
        campaign = Campaign.query.get('spotify')
        campaign.status = 'INACTIVE'
        db.session.commit()

    # Should not return spotify campaign even for US users
    response = client.get('/api/v1/delivery?app=com.anyapp&country=us&os=web')
    data = response.json if response.status_code == 200 else []
    assert not any(c['cid'] == 'spotify' for c in data)