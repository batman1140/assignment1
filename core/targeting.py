from typing import List
import functools
import time
from .models import Campaign, TargetingRule
from .extensions import db
from flask import current_app

def cache_campaigns(timeout=300):  # 5 minutes cache
    """Decorator to cache campaign results"""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            cache = getattr(current_app, 'campaign_cache', {})
            cache_key = f"{args[0]}:{args[1]}:{args[2]}"
            
            # Check cache
            if cache_key in cache:
                result, timestamp = cache['key']
                if time.time() - timestamp < timeout:
                    return result
            
            # Get fresh result
            result = f(*args, **kwargs)
            cache[cache_key] = (result, time.time())
            
            # Prune old entries if cache is too large
            if len(cache) > 1000:  # Keep cache size reasonable
                old_keys = sorted(
                    cache.keys(),
                    key=lambda k: cache[k][1]
                )[:len(cache)//2]
                for k in old_keys:
                    del cache[k]
            
            return result
        return wrapper
    return decorator

@cache_campaigns()
def get_matching_campaigns(app_id: str, country: str, os: str) -> List[Campaign]:
    """
    Get all active campaigns that match the given targeting criteria.
    Optimized for read-heavy workloads with caching and efficient querying.
    """
    # Get all active campaigns with their rules
    active_campaigns = (
        Campaign.query
        .filter_by(status="ACTIVE")
        .all()
    )
    
    matching_campaigns = []
    seen_campaigns = set()  # To avoid duplicates

    for campaign in active_campaigns:
        if campaign.id in seen_campaigns:
            continue
            
        # Check each rule for this campaign
        for rule in campaign.targeting_rules:
            if rule.matches(app_id, country, os):
                matching_campaigns.append(campaign)
                seen_campaigns.add(campaign.id)
                break  # No need to check other rules once we have a match

    return matching_campaigns

def invalidate_campaign_cache(campaign_id: str = None):
    """
    Invalidate the campaign cache when campaign data changes.
    If campaign_id is None, invalidate entire cache.
    """
    cache = getattr(current_app, 'campaign_cache', {})
    if campaign_id:
        # Remove specific campaign entries
        keys_to_remove = [k for k in cache.keys() if campaign_id in k]
        for k in keys_to_remove:
            del cache[k]
    else:
        # Clear entire cache
        cache.clear()