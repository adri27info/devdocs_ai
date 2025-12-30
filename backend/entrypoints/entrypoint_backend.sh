#!/bin/bash

set -e

# HOSTS & PORTS
DB_HOST="db"
DB_PORT="5432"
REDIS_HOST="redis"
REDIS_PORT="6379"

# Location of the stripe webhook env file. This env is builded in runtime
SECRET_FILE="/app/stripe_secret/stripe_webhook.env"

# PYTHON CONF
APP_PATH="/app/devdocs_ai"
MANAGE_PY="$APP_PATH/manage.py"

export PYTHONPATH="$APP_PATH:$PYTHONPATH"

# FUNCTIONS
cleanup() {
  echo "Container stopping..."

  if [ "$USE_EC2" = "True" ]; then
    echo "Stopping EC2 instance..."
    python "$MANAGE_PY" handle_ec2_service stop || true
  else
    echo "USE_EC2=False, skipping EC2 stop"
  fi
}

# Capture Docker stop signals
trap cleanup SIGTERM SIGINT

wait_for_service() {
  host=$1
  port=$2
  echo "Waiting for $host:$port to be available..."
  while ! nc -z "$host" "$port"; do
    sleep 3
  done
  echo "$host:$port is available."
}

wait_for_stripe_webhook_secret() {
  echo "Waiting for STRIPE_WEBHOOK_SECRET..."
  while [ ! -f "$SECRET_FILE" ]; do
    sleep 1
  done

  export $(cat "$SECRET_FILE")
  echo "STRIPE_WEBHOOK_SECRET loaded: $STRIPE_WEBHOOK_SECRET"
}

initialize_database() {
  echo "Initializing database..."
  if ! python $MANAGE_PY create_devdocs_ai_db; then
    echo "Database initialization failed. Please check database" \
      "configuration and migrations." >&2
    exit 1
  fi
}

collect_static_files() {
  if [ "$USE_S3" = "True" ]; then
    echo "Using S3 for static files..."
    python $MANAGE_PY collectstatic --noinput
  fi
}

start_ec2() {
  if [ "$USE_EC2" = "True" ]; then
    echo "Starting EC2 instance..."
    python $MANAGE_PY handle_ec2_service start
  else
    echo "USE_EC2=False, skipping EC2 start"
  fi
}

start_django_server() {
  echo "Starting Django server with HTTP..."
  python "$MANAGE_PY" runserver 0.0.0.0:8000 &
  DJANGO_PID=$!
  wait $DJANGO_PID
}

main() {
  wait_for_service $DB_HOST $DB_PORT
  initialize_database
  wait_for_service $REDIS_HOST $REDIS_PORT
  wait_for_stripe_webhook_secret
  collect_static_files
  start_ec2
  start_django_server
}

main