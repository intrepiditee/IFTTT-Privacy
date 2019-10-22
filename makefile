all:
	docker-compose build
	docker-compose up --scale sensor=3

clean:
	docker-compose down
