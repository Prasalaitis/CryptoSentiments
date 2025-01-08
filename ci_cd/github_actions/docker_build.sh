#!/bin/bash
set -e

IMAGE_NAME="reddit-ingestion-app"
DOCKER_USER="<your-docker-username>"
DOCKER_TAG="latest"

echo "Building Docker image..."
docker build -t $IMAGE_NAME .

echo "Tagging Docker image..."
docker tag $IMAGE_NAME:latest $DOCKER_USER/$IMAGE_NAME:$DOCKER_TAG

echo "Pushing Docker image..."
docker push $DOCKER_USER/$IMAGE_NAME:$DOCKER_TAG

echo "Docker image pushed successfully: $DOCKER_USER/$IMAGE_NAME:$DOCKER_TAG"
