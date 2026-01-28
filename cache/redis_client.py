import redis
from loguru import logger

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True) # decode_responses ensures strings are returned instead of bytes)

def check_redis() -> bool:
    try:
        pong = redis_client.ping()
        logger.info("Redis connection successful.")
        return pong
    except redis.ConnectionError as e:
        logger.error(f"Redis connection failed: {e}")
        return False

if __name__ == "__main__":
    check_redis()