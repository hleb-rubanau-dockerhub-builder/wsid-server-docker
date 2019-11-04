IMAGE_NAME=wsid-identity-server
IMAGE_VERSION=0.0.1
IMAGE_ID=${IMAGE_NAME}:${IMAGE_VERSION}

image:
	docker build -t ${IMAGE_ID} .

test: image
	docker run --rm -it ${IMAGE_ID} /bin/bash -c 'env | grep WSID'

bash: image
	docker run --rm -it --entrypoint=/bin/bash ${IMAGE_ID} 

up: 
	docker-compose up -d --build
