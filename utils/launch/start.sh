#!/bin/bash

set -e

# GENERAL PATHS
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
BACKEND_DIR="$SCRIPT_DIR/../../backend"
FRONTEND_DIR="$SCRIPT_DIR/../../frontend"

# FUNCTIONS
start_backend_containers() {
  echo "Starting backend containers ..."
  (cd "$BACKEND_DIR" && docker-compose up --build -d)
}

start_frontend_containers() {
  echo "Starting frontend containers ..."
  (cd "$FRONTEND_DIR" && docker-compose up --build -d)
}

main() {
  start_backend_containers
  start_frontend_containers
  echo "All containers are running."
}

main
