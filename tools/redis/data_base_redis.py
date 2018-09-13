import redis
import configparser
import os
from tools.security.decrypt import AESCipher
from aichatbot.settings import BASE_DIR
from redis import StrictRedis

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


def connect(password=True):
    if password:
        conn = redis.Redis(redis_host, redis_port, redis_db, redis_password)
    else:
        conn = redis.Redis(redis_host, redis_port, redis_db, '')
    return conn


def get_redis(key, conn=None):
    if conn is None:
        conn = connect()
    return conn.get(key)


def set_redis(key, value, conn=None):
    if conn is None:
        conn = connect()
    conn.set(key, value)


if __name__ == "__main__":
    # conn = connect()
    # set_redis('name', 'rick', conn)
    # print(get_redis('name', conn))
    redis = StrictRedis(host=redis_host, port=int(redis_port), db=redis_db, password=redis_password)
    # redis = StrictRedis(host=redis_host, port=int(redis_port), db=redis_db)
    redis.set('name','rick')
    print(redis.get('name').decode('utf-8'))
