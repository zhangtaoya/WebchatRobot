import mongo
import motordb
import redis
from config import config


def get_redis(db=0):
    redis_cli = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=db,
                            password=config.REDIS_PASSWORD)
    return redis_cli


def get_col_test_my():
    return motordb.mongo_collection('test', 'my', config.DB_HOST, config.DB_PORT)


def get_col_wechat_account():
    return motordb.mongo_collection('wechat_robot', 'wechat_account', config.DB_HOST, config.DB_PORT)


def get_col_wechat_account_sync():
    return mongo.mongo_collection('wechat_robot', 'wechat_account', config.DB_HOST, config.DB_PORT)
