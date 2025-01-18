import aioredis
import json

redis = None

async def init_redis():
    global redis
    redis = await aioredis.from_url("redis://redis:6379", decode_responses=True)

async def cache_item(item):
    await redis.set(
        f"item:{item.id}",
        json.dumps({"id": item.id, "name": item.name, "description": item.description}),
    )

async def get_cached_item(item_id):
    item_data = await redis.get(f"item:{item_id}")
    if item_data:
        return json.loads(item_data)
    return None
