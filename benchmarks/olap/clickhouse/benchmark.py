from clickhouse_driver import Client

from benchmarks.olap.common_utils.test_queries import QUERIES
from benchmarks.olap.common_utils.timer import timer
from benchmarks.olap.config import BENCHMARK_ITERATIONS, CLICKHOUSE_HOST

client = Client(CLICKHOUSE_HOST)


@timer(BENCHMARK_ITERATIONS)
def execute_query(query: str):
    client.execute(query)


def run_benchmarks():
    print('Running benchmarks for Clickhouse:\n')
    for name, query in QUERIES.items():
        print(f'"{name}"')
        execute_query(query)
    print('----- Done! -----\n')


if __name__ == '__main__':
    run_benchmarks()
