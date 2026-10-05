import json
import os

import redis


REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0",
)

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
)


def get_cached_tasks():
    data = redis_client.get("tasks")

    if data:
        return json.loads(data)

    return None


def cache_tasks(tasks):
    redis_client.set(
        "tasks",
        json.dumps(tasks),
        ex=60,
    )


def clear_task_cache():
    redis_client.delete("tasks")