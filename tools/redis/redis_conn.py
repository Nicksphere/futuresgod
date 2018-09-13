import sys
from rediscluster import StrictRedisCluster
from redis import StrictRedis
from redis import *
import conf.logger_config as log_conf
import conf.path_config as config
import redis
import configparser
import os
from tools.security.decrypt import AESCipher
from aichatbot.settings import BASE_DIR
from redis import StrictRedis

logger = log_conf.get_logger_root()

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'conf/chatbot.conf'))
keyMaterial = config.get("crypto", "keymaterial")
secondkey = config.get("crypto", "key")
AESProcess = AESCipher(keyMaterial, secondkey)
redis_host = config.get("redis", "host")
redis_port = config.get("redis", "port")
redis_db = config.get("redis", "db")
redis_password_ = config.get("redis", "password")
redis_password = AESProcess.decryptkey(redis_password_).decode()

try:
    #redisconn = StrictRedisCluster(startup_nodes=config.redis_nodes, password=config.redis_password)
    # redisconn = StrictRedis(host='127.0.0.1', port=6379)
    #redisconn = StrictRedisCluster(startup_nodes=config.redis_nodes, decode_responses=True)
    redisconn = StrictRedis(host=redis_host, port=int(redis_port), db=redis_db, password=redis_password)
except Exception as e:
    logger.error(e)
    sys.exit(1)
