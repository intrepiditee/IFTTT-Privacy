all:
	docker-compose build
	docker-compose up --scale switch=3 --scale sensor=3

clean:
	docker-compose down
