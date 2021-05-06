from multiprocessing import Pool

import tqdm as tqdm
from clickhouse_driver import Client

from benchmarks.olap.common_utils.fake_data_gen import Row, generate_fake_data
from benchmarks.olap.config import CLICKHOUSE_HOST, NUMBER_OF_BATCHES, UPLOAD_BATCH_SIZE

client = Client(CLICKHOUSE_HOST)


def upload_batch(batch):
    columns = ', '.join(Row._fields)
    client.execute(
        f'INSERT INTO views ({columns}) VALUES',
        batch
    )


if __name__ == '__main__':
    print('Uploading test data to Clickhouse:')
    test_data = generate_fake_data(UPLOAD_BATCH_SIZE, NUMBER_OF_BATCHES)

    with Pool() as pool:
        r = list(tqdm.tqdm(
            pool.imap(upload_batch, test_data),
            total=NUMBER_OF_BATCHES
        ))
