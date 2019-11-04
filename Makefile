IMAGE_NAME=wsid-identity-server
IMAGE_VERSION=0.0.1
IMAGE_ID=${IMAGE_NAME}:${IMAGE_VERSION}

image:
	docker build -t ${IMAGE_ID} .

test: image
    docker run -rm -it ${IMAGE_ID}	 /bin/bash
