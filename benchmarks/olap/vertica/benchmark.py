import vertica_python

from benchmarks.olap.common_utils.test_queries import QUERIES
from benchmarks.olap.common_utils.timer import timer
from benchmarks.olap.config import BENCHMARK_ITERATIONS, VERTICA_CONNECTION_PARAMS


@timer(BENCHMARK_ITERATIONS)
def execute_query(query: str):
    with vertica_python.connect(**VERTICA_CONNECTION_PARAMS) as connection:
        cursor = connection.cursor()
        cursor.execute(query)


def run_benchmarks():
    print('Running benchmarks for Vertica:\n')
    for name, query in QUERIES.items():
        print(f'"{name}"')
        execute_query(query)
    print('----- Done! -----\n')


if __name__ == '__main__':
    run_benchmarks()
