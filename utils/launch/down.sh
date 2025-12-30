#!/bin/bash

set -e

# GENERAL PATHS
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
BACKEND_DIR="$SCRIPT_DIR/../../backend"
FRONTEND_DIR="$SCRIPT_DIR/../../frontend"

# COMPOSE FILES
BACKEND_COMPOSE_FILE="$BACKEND_DIR/docker-compose.yml"
FRONTEND_COMPOSE_FILE="$FRONTEND_DIR/docker-compose.yml"

# FUNCTIONS
stop_backend_containers() {
  echo "Stopping and removing backend containers ..."
  # The timeout is set to 120 seconds to allow graceful shutdown of all services
  docker-compose -f "$BACKEND_COMPOSE_FILE" down --timeout 120
}

stop_frontend_containers() {
  echo "Stopping and removing frontend containers ..."
  docker-compose -f "$FRONTEND_COMPOSE_FILE" down
}

cleanup_volumes() {
  echo "Deleting unused volumes..."
  docker volume prune -f
}

main() {
  stop_backend_containers
  stop_frontend_containers
  cleanup_volumes
  echo "Process completed."
}

main
