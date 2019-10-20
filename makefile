all:
	docker swarm init
	docker stack deploy --compose-file docker-compose.yml ifttt

clean:
	docker stack rm ifttt
	docker swarm leave --force
