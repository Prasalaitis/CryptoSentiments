#!/bin/bash
set -e

SERVER_USER="<your-server-user>"
SERVER_HOST="<your-server-ip>"
PROJECT_DIR="/path/to/project"
DOCKER_COMPOSE_FILE="docker-compose.yml"

echo "Deploying to server: $SERVER_USER@$SERVER_HOST"

# Copy updated files to the server
echo "Uploading files..."
scp docker-compose.yml $SERVER_USER@$SERVER_HOST:$PROJECT_DIR

# Restart services on the server
echo "Restarting services..."
ssh $SERVER_USER@$SERVER_HOST << EOF
  cd $PROJECT_DIR
  docker-compose pull
  docker-compose up -d
EOF

echo "Deployment completed successfully!"
