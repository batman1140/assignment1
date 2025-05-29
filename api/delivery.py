from flask import Blueprint, jsonify, request
from core.targeting import get_matching_campaigns
from core.utils import track_request_metrics, track_campaign_match

delivery_bp = Blueprint('delivery', __name__)

@delivery_bp.route('/api/v1/delivery', methods=['GET'])
@track_request_metrics
def get_delivery():
    """
    Get matching campaigns for the given request parameters.
    Query parameters:
    - app or app_id: The ID of the requesting app (e.g., com.example.app)
    - country: The country code of the user (e.g., US, IN)
    - os: The operating system of the user (e.g., android, ios, web)
    """
    # Accept either 'app' or 'app_id' parameter
    app_id = request.args.get('app_id') or request.args.get('app')
    country = request.args.get('country', '').upper()
    os = request.args.get('os', '').lower()

    # Validate required parameters
    if not app_id:
        return jsonify({'error': 'missing app param'}), 400
    if not country:
        return jsonify({'error': 'missing country param'}), 400
    if not os:
        return jsonify({'error': 'missing os param'}), 400

    # Get matching campaigns
    matching_campaigns = get_matching_campaigns(app_id, country, os)
    
    if not matching_campaigns:
        return '', 204  # No content

    # Track matches for metrics
    for campaign in matching_campaigns:
        track_campaign_match(campaign.id)

    # Return all matching campaigns
    return jsonify([campaign.to_dict() for campaign in matching_campaigns]), 200