run:
	docker-compose up -d

stop:
	docker-compose down

seed_db:
	export PYTHONPATH="${PYTHONPATH}:${PWD}/../.." \
	&& python -m clickhouse.seed_db \
	&& python -m vertica.seed_db

run_benchmarks:
	export PYTHONPATH="${PYTHONPATH}:${PWD}/../.." \
	&& python -m clickhouse.benchmark \
	&& python -m vertica.benchmark
