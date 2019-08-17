import os
import redis

# Configure Redis
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', 6379)
redis_db = redis.StrictRedis(host=redis_host, 
    port=redis_port, db=0, charset="utf-8", decode_responses=True)


def db_init(session_id):
    redis_db.set(session_id, '')

def db_save(session_id, data):
    # Data are saved as Strings
    redis_db.append(session_id, f"*{str(data)}")

def db_retrieve(session_id):
    response = redis_db.get(session_id).split('*')
    while '' in response:
        response.remove('')
    return response

def db_delete(session_id):
    return redis_db.delete(session_id) # Deletes key from Redis