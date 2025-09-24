import json
from typing import Annotated

from app.core.logging.logging import get_logger
from app.core.taskiq.broker import broker
from app.dependencies.redis_dependency import RedisDependency
from taskiq import TaskiqDepends

logger = get_logger()


@broker.task
async def send_telegram(
    text: str,
    user_id: int,
    redis: Annotated[RedisDependency, TaskiqDepends(RedisDependency)],
):
    payld = {
        "text": text,
        "user_id": user_id,
    }
    async with redis.get_client() as client:
        await client.publish("telegram_queue", json.dumps(payld))
