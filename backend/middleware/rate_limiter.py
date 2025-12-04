# ========================
# Rate Limiting Middleware
# ========================

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple


class RateLimiter:
    """
    Rate limiting middleware to prevent abuse
    
    Rules:
    - 10 requests per minute per user (authenticated)
    - 5 requests per minute per IP (unauthenticated)
    - 429 status when limit exceeded
    """
    
    def __init__(self):
        # Store: {identifier: [(timestamp1, timestamp2, ...)]}
        self.request_history: Dict[str, list] = defaultdict(list)
        self.cleanup_interval = 60  # Clean old entries every 60 seconds
        self.last_cleanup = datetime.now()
        
    def _cleanup_old_entries(self):
        """Remove entries older than 1 minute"""
        now = datetime.now()
        if (now - self.last_cleanup).seconds < self.cleanup_interval:
            return
            
        cutoff = now - timedelta(minutes=1)
        for identifier in list(self.request_history.keys()):
            self.request_history[identifier] = [
                ts for ts in self.request_history[identifier] 
                if ts > cutoff
            ]
            # Remove empty entries
            if not self.request_history[identifier]:
                del self.request_history[identifier]
        
        self.last_cleanup = now
    
    def is_rate_limited(self, identifier: str, limit: int = 10) -> Tuple[bool, int]:
        """
        Check if identifier has exceeded rate limit
        
        Args:
            identifier: User email or IP address
            limit: Max requests per minute
            
        Returns:
            (is_limited, remaining_requests)
        """
        self._cleanup_old_entries()
        
        now = datetime.now()
        cutoff = now - timedelta(minutes=1)
        
        # Get recent requests (within last minute)
        recent_requests = [
            ts for ts in self.request_history[identifier] 
            if ts > cutoff
        ]
        
        # Update history
        self.request_history[identifier] = recent_requests
        
        # Check limit
        if len(recent_requests) >= limit:
            return True, 0
        
        # Add current request
        self.request_history[identifier].append(now)
        
        remaining = limit - len(recent_requests) - 1
        return False, max(0, remaining)


# Global instance
rate_limiter = RateLimiter()


async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware to enforce rate limiting
    
    Uses IP address for all requests (simpler approach)
    Auth endpoints have stricter limits
    """
    # Skip rate limiting for health check
    if request.url.path == "/health":
        return await call_next(request)
    
    # Get IP address as identifier
    identifier = request.client.host
    
    # Set limit based on endpoint
    if request.url.path.startswith("/auth"):
        limit = 5  # Auth endpoints: 5 req/min
    else:
        limit = 10  # Other endpoints: 10 req/min
    
    # Check rate limit
    is_limited, remaining = rate_limiter.is_rate_limited(identifier, limit)
    
    if is_limited:
        return JSONResponse(
            status_code=429,
            content={
                "detail": f"Rate limit exceeded. Max {limit} requests per minute. Try again in 60 seconds.",
                "retry_after": 60
            },
            headers={
                "Retry-After": "60",
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": "0"
            }
        )
    
    # Process request
    response = await call_next(request)
    
    # Add rate limit headers to response
    response.headers["X-RateLimit-Limit"] = str(limit)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    
    return response
