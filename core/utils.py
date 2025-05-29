"""Utility functions for monitoring and performance."""
from functools import wraps
import time
from prometheus_client import Counter, Histogram

# Define metrics
REQUEST_COUNT = Counter(
    'campaign_delivery_requests_total',
    'Total number of campaign delivery requests',
    ['endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'campaign_delivery_request_duration_seconds',
    'Request duration in seconds',
    ['endpoint']
)

CAMPAIGN_MATCHES = Counter(
    'campaign_matches_total',
    'Total number of campaign matches',
    ['campaign_id']
)

CACHE_HITS = Counter(
    'campaign_cache_hits_total',
    'Total number of cache hits'
)

CACHE_MISSES = Counter(
    'campaign_cache_misses_total',
    'Total number of cache misses'
)

def track_request_metrics(f):
    """Decorator to track request metrics"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            response = f(*args, **kwargs)
            status_code = str(response[1]) if isinstance(response, tuple) else '200'
        except Exception as e:
            status_code = '500'
            raise e
        finally:
            # Record metrics
            REQUEST_COUNT.labels(
                endpoint=f.__name__,
                status_code=status_code
            ).inc()
            
            REQUEST_LATENCY.labels(
                endpoint=f.__name__
            ).observe(time.time() - start_time)
            
        return response
    return wrapper

def track_campaign_match(campaign_id: str):
    """Track when a campaign matches"""
    CAMPAIGN_MATCHES.labels(campaign_id=campaign_id).inc()

def track_cache_metrics(hit: bool):
    """Track cache hit/miss metrics"""
    if hit:
        CACHE_HITS.inc()
    else:
        CACHE_MISSES.inc()