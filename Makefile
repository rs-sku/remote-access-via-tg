build:
	docker build -t service:latest .

build_virus:
	docker build -t virus:latest virus

up_tp:
	docker compose -f docker-compose.tp.yml up -d

up:
	docker compose up -d

up_virus:
	docker run -d --rm --name virus --env-file virus/.env virus:latest 

down_virus:
	docker stop virus

down_tp:
	docker compose -f docker-compose.tp.yml down

down:
	docker compose down

client:
	docker run --env-file .env --rm -it service:latest python run_api_client.py

lint:
	black --check -l 120 app tests
	isort --check --line-length 120 .
	pylint --rcfile conf/.pylintrc app
	mypy ${PWD}/app

fix:
	black -l 120 app tests
	isort --line-length 120 .
	pylint --rcfile conf/.pylintrc app
	mypy --strict app

tdb:
	docker run -d -p "5431:5432" --rm -e POSTGRES_PASSWORD=postgres --name test_db postgres:16.3

test:
	pytest --cov=app