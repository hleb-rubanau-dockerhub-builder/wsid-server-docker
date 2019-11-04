IMAGE_NAME=wsid-identity-server
IMAGE_VERSION=0.0.1

image:
	docker build -t ${IMAGE_NAME}:${IMAGE_VERSION} .
	
