import hashlib
import json
from typing import Any, Optional
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

class NarrativeCache:
    """Cache for AI-generated narratives based on data hash"""
    
    def __init__(self, max_size: int = 100):
        self._cache = {}
        self._max_size = max_size
    
    def _generate_hash(self, data: Any) -> str:
        """Generate hash from data for cache key"""
        try:
            # Convert to JSON string for consistent hashing
            json_str = json.dumps(data, sort_keys=True, default=str)
            return hashlib.sha256(json_str.encode()).hexdigest()[:16]
        except Exception as e:
            logger.warning(f"Hash generation failed: {e}")
            return None
    
    def get(self, data: Any) -> Optional[str]:
        """Get cached narrative if exists"""
        cache_key = self._generate_hash(data)
        if not cache_key:
            return None
        
        if cache_key in self._cache:
            logger.info(f"Cache HIT: {cache_key}")
            return self._cache[cache_key]
        
        logger.info(f"Cache MISS: {cache_key}")
        return None
    
    def set(self, data: Any, narrative: str) -> None:
        """Store narrative in cache"""
        cache_key = self._generate_hash(data)
        if not cache_key:
            return
        
        # Simple LRU: remove oldest if at capacity
        if len(self._cache) >= self._max_size:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
            logger.info(f"Cache eviction: {oldest_key}")
        
        self._cache[cache_key] = narrative
        logger.info(f"Cache SET: {cache_key}")
    
    def clear(self) -> None:
        """Clear all cache"""
        self._cache.clear()
        logger.info("Cache cleared")
    
    def size(self) -> int:
        """Get current cache size"""
        return len(self._cache)

# Global cache instance
narrative_cache = NarrativeCache(max_size=100)
