import argparse
import asyncio

import aioredis  # type: ignore
import logstash
import motor.motor_asyncio  # type: ignore
import sanic.log
import sentry_sdk
from aiokafka import AIOKafkaProducer  # type: ignore

from endpoints import ugc_api
from helpers import RequestIdFilter
from middlewares import auth_middleware
from sanic import Sanic
from sentry_sdk.integrations.sanic import SanicIntegration
from serializers import serializer
from settings import (API_SENTRY_DSN, COMPRESSION_TYPE,
                      KAFKA_BOOTSTRAP_SERVERS, KAFKA_PRODUCER_PASSWORD,
                      KAFKA_PRODUCER_USERNAME, LOGSTASH_HOST, LOGSTASH_PORT,
                      MAX_BATCH_SIZE, MONGO_CONNECT_URI, MONGO_DB_NAME,
                      REDIS_CACHE_DB, REDIS_HOST, REDIS_PORT)

sentry_sdk.init(dsn=API_SENTRY_DSN, integrations=[SanicIntegration()])
app = Sanic(__name__)

app.blueprint(ugc_api)
app.register_middleware(auth_middleware, 'request')

sanic.log.access_logger.addFilter(RequestIdFilter())
sanic.log.access_logger.addHandler(logstash.LogstashHandler(LOGSTASH_HOST, LOGSTASH_PORT, version=1))


@app.listener('before_server_start')
async def on_startup(app: Sanic, loop: asyncio.AbstractEventLoop):
    app.ctx.producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                        loop=loop,
                                        value_serializer=serializer,
                                        compression_type=COMPRESSION_TYPE,
                                        max_batch_size=MAX_BATCH_SIZE,
                                        security_protocol='SASL_PLAINTEXT',
                                        sasl_mechanism='SCRAM-SHA-512',
                                        sasl_plain_username=KAFKA_PRODUCER_USERNAME,
                                        sasl_plain_password=KAFKA_PRODUCER_PASSWORD
                                        )
    await app.ctx.producer.start()
    app.ctx.redis = await aioredis.create_redis_pool((REDIS_HOST, REDIS_PORT), db=REDIS_CACHE_DB)
    app.ctx.mongo = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONNECT_URI)[MONGO_DB_NAME]


@app.listener('before_server_stop')
async def on_shutdown(app: Sanic, loop: asyncio.AbstractEventLoop):
    await app.ctx.producer.stop()
    app.ctx.redis.close()
    await app.ctx.redis.wait_closed()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=9001)
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port, access_log=True)
