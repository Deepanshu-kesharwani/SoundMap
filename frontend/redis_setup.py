import os
# import redis
#
# redis_client = redis.Redis(
#     # host=os.getenv("REDIS_HOST"),
#     # port=int(os.getenv("REDIS_PORT")),
#     # password=os.getenv("REDIS_PASSWORD"),
#     # decode_responses=True,
#     # ssl=False  # VERY important since it's using `rediss://`
import redis

redis_client = redis.Redis(
    host="red-d0h4740dl3ps73chpm00",
    port=6379,
    decode_responses=True
)


