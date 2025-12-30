#!/bin/sh

set -e

# HOST & PORT
REDIS_HOST="redis"
REDIS_PORT="6379"

# PYTHON CONF
APP_PATH="/app/devdocs_ai"

# Location of the stripe webhook env file. This env is builded in runtime
SECRET_FILE="/app/stripe_secret/stripe_webhook.env"

export PYTHONPATH="$APP_PATH:$PYTHONPATH"

# FUNCTIONS
wait_for_service() {
  host=$1
  port=$2
  echo "Waiting for $host:$port to be available..."
  while ! nc -z "$host" "$port"; do
    sleep 1
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

start_celery_worker() {
  echo "Starting Celery worker..."
  celery -A devdocs_ai.celery_app worker --loglevel=info
}

main() {
  wait_for_service $REDIS_HOST $REDIS_PORT
  wait_for_stripe_webhook_secret
  start_celery_worker
}

main