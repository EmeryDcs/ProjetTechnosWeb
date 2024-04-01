import redis

redis_url = "redis://localhost:6379/0"
redis_client = redis.from_url(redis_url)

def get_order_status(order_id):
    return redis_client.get(f'order:{order_id}')

def set_order_status(order_id, status):
    return redis_client.set(f'order:{order_id}', status)

def delete_order_status(order_id):
    return redis_client.delete(f'order:{order_id}')
