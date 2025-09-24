from core.config import REDIS_URL
from redis.asyncio import Redis

redis = Redis.from_url(REDIS_URL, decode_responses=True)
