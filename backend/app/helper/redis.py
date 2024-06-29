import json

from helper import get_redis_engine

def init_value(name, value):
    payload = json.dumps(value)
    redis = get_redis_engine()
    # For initialize the publisher
    redis.publish(name, payload)
    # Save information to redis db
    redis.set(name, payload)
    return None

def update_value(name, value):
    payload = json.dumps(value)
    redis = get_redis_engine()
    redis.publish(name, payload)
    # Save information to redis db
    redis.set(name, payload)
    return None

def get_value(name):
    redis = get_redis_engine()
    return json.loads(redis.get(name))
