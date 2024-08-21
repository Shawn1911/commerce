# abcdefghijklmnopqrstuvwxyz
from redis import Redis


redis_client = Redis(host='localhost', port=6379, db=0)
redis_client.ping()
