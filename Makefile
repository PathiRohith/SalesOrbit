start:
	docker-compose up --build -d

stop:
	docker-compose down

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	black --check .

test:
	docker-compose exec sales-api pytest --cov=agents --cov=rag --cov=workers

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} +