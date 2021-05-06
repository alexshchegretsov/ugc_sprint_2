import json

import requests
import sentry_sdk
from kafka import KafkaConsumer  # type: ignore

from settings import USERS_VIEWS_FILMS_TOPIC, KAFKA_BOOTSTRAP_SERVERS, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD, \
    CLICKHOUSE_URL, KAFKA_CONSUMER_USERNAME, KAFKA_CONSUMER_PASSWORD, ETL_SENTRY_DSN

sentry_sdk.init(dsn=ETL_SENTRY_DSN, traces_sample_rate=1.0)


def main():
    auth = {
        'X-ClickHouse-User': CLICKHOUSE_USER,
        'X-ClickHouse-Key': CLICKHOUSE_PASSWORD,
    }

    consumer = KafkaConsumer(USERS_VIEWS_FILMS_TOPIC,
                             group_id='views_consumer',
                             bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
                             security_protocol='SASL_PLAINTEXT',
                             sasl_mechanism='SCRAM-SHA-512',
                             sasl_plain_password=KAFKA_CONSUMER_PASSWORD,
                             sasl_plain_username=KAFKA_CONSUMER_USERNAME,
                             value_deserializer=lambda m: json.loads(m))
    to_click = []
    for msg in consumer:
        to_click.append(msg.value)

        if msg.offset % 1000 == 0:
            rs = requests.post(url=CLICKHOUSE_URL, headers=auth, data=json.dumps(to_click))    # format JSONEachRow
            rs.raise_for_status()
            to_click.clear()


if __name__ == '__main__':
    main()
