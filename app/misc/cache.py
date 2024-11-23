import redis
from app.settings import redis_handler, app, logger


class DataCache:
    """
    A class for managing Redis cache operations.

    Attributes:
        rd (redis.Redis): A Redis client instance.
    """

    def __init__(self,) -> None:
        self.rd = redis_handler

    def set_cache(self, cache_id: str, cache_value: str) -> None:
        """
        Sets a value in Redis cache with a specified expiration time.

        Args:
            cache_id (str): The unique identifier for the cache entry.
            cache_value (str): The value to be stored in the cache.

        Returns:
            None
        """

        try:
            self.rd.set(
                cache_id, cache_value, ex=int(app.config["REDIS_EXPIRY"]))
        except redis.RedisError as e:
            logger.error(
                msg=f"[SET CACHE] Error occured setting cache data due to {e}")
            return None

    def get_cache(self, cache_id: str) -> str:
        """
        Retrieves a value from Redis cache.

        Args:
            cache_id (str): The unique identifier for the cache entry.

        Returns:
            str: The cached value, or None if the key doesn't exist or
            an error occurs.
        """

        try:
            result = self.rd.get(cache_id)
            return result or None
        except redis.exceptions.RedisError as e:
            logger.error(
                msg=f"[GET CACHE] Error occured getting cache data due to {e}")
            return None
