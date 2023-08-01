run: 
	poetry run streamlit run main.py

start-ngrok:
	ngrok http 8501 

stop-ngrok:
	killall ngrok

compose-run:
	echo "Starting containers with compose..."
	docker-compose up -d --build

compose-stop:
	echo "Stopping containers..."
	docker-compose down --remove-orphans 

compose-logs:
	docker-compose logs -f

black:
	poetry run black .

isort:
	poetry run isort --profile black . 

format:
	make isort
	make black

test:
	pytest tests/
	
start:
	- make compose-stop
	- make compose-run
	

# Start with --debug flag True

run-debug:
	- export DEBUG=True
	- make start
	make compose-logs
