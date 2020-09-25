import os
from arq.connections import RedisSettings

# default variables are for testing, docker populates runtime variables
REDIS_SETTINGS = RedisSettings(host=os.getenv("REDIS_IP", 'localhost'),
                               port=os.getenv("REDIS_PORT", 6379))
