docker:
	sudo docker build -t fluidserver .

docker-doas:
	doas docker build -t fluidserver .