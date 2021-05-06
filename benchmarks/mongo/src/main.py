from benchmarks.mongo.src.test_scenarios import READ_SCENARIOS, WRITE_SCENARIOS

if __name__ == '__main__':
    print('Running read benchmarks for Mongo...\n')

    for scenario in READ_SCENARIOS:
        func = scenario.get('func')
        kwargs = scenario.get('kwargs')
        func(**kwargs)

    print('Done!\n')

    print('Running write benchmarks for Mongo...\n')

    for scenario in WRITE_SCENARIOS:
        func = scenario.get('func')
        kwargs = scenario.get('kwargs')
        func(**kwargs)

    print('Done!\n')
