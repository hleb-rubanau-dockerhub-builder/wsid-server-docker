IMAGE_NAME=wsid-identity-server
IMAGE_VERSION=0.0.1
IMAGE_ID=${IMAGE_NAME}:${IMAGE_VERSION}

image:
	docker build -t ${IMAGE_ID} .

bash: image
	docker run --rm -it --entrypoint=/bin/bash ${IMAGE_ID} 

up: 
	docker-compose up -d --build --remove-orphans && docker-compose logs

down:
	docker-compose down -v

test: down up
	./test.sh
