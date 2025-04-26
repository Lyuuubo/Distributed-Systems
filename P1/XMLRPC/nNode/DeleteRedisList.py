import redis

client_redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

client_redis.ltrim('insult_list_n', 1, 0)
client_redis.ltrim('work_queue', 1, 0)
client_redis.ltrim('result_queue', 1, 0)