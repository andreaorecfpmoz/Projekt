import redis
import json

redis_client = None


async def init_redis():
    global redis_client
    redis_client = redis.asyncio.StrictRedis(host='localhost', port=6379, db=0)


async def cache_item(item):
    await redis_client.set(
        f"item:{item.id}",
        json.dumps({"id": item.id, "name": item.name, "description": item.description}),
    )


async def get_cached_item(item_id):
    item_data = await redis_client.get(f"item:{item_id}")
    if item_data:
        return json.loads(item_data)
    return None

