from multiprocessing import Pool

import tqdm
import vertica_python

from benchmarks.olap.common_utils.fake_data_gen import Row, generate_fake_data
from benchmarks.olap.config import NUMBER_OF_BATCHES, UPLOAD_BATCH_SIZE, VERTICA_CONNECTION_PARAMS


def upload_batch(batch):
    with vertica_python.connect(**VERTICA_CONNECTION_PARAMS) as connection:
        columns = ', '.join(Row._fields)
        placeholders = ', '.join(['%s'] * len(Row._fields))
        cursor = connection.cursor()
        cursor.executemany(
            f'INSERT INTO views ({columns}) VALUES ({placeholders})',
            batch
        )


if __name__ == '__main__':
    print('Uploading test data to Vertica:')
    test_data = generate_fake_data(UPLOAD_BATCH_SIZE, NUMBER_OF_BATCHES)
    with Pool() as pool:
        r = list(tqdm.tqdm(
            pool.imap(upload_batch, test_data),
            total=NUMBER_OF_BATCHES
        ))
