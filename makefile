all:
	docker swarm init
	docker image build -f sensor/dockerfile -t ifttt_sensor sensor/
	docker image build -f server/dockerfile -t ifttt_server server/
	docker image build -f switch/dockerfile -t ifttt_switch switch/
	docker image build -f tester/dockerfile -t ifttt_tester tester/
	docker stack deploy --compose-file docker-compose.yml ifttt

clean:
	docker stack rm ifttt
	docker swarm leave --force
