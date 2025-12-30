#!/bin/sh
set -e

# STRIPE WEBHOOK URL
FORWARD_URL="${STRIPE_FORWARD_URL:-http://backend:8000/payments/webhook/}"

# Location of the stripe webhook env file. This env is builded in runtime
SECRET_FILE="/app/stripe_secret/stripe_webhook.env" 

# FUNCTIONS
start_stripe_service() {
  if [ "$USE_STRIPE" = "True" ] && [ -n "$STRIPE_SECRET_KEY" ]; then
    echo "Stripe service enabled and secret key found."
    echo "Starting Stripe CLI..."

    stripe listen --forward-to "$FORWARD_URL" --api-key "$STRIPE_SECRET_KEY" 2>&1 | while read -r line; do
      echo "$line"
      if echo "$line" | grep -q "whsec_"; then
        secret=$(echo "$line" | grep -oE 'whsec_[a-zA-Z0-9]+')
        echo "STRIPE_WEBHOOK_SECRET=$secret" > "$SECRET_FILE"
        chmod 644 "$SECRET_FILE"
        echo "Webhook secret written to $SECRET_FILE"
      fi
    done
  else
    echo "Stripe service disabled or STRIPE_SECRET_KEY not set. Skipping Stripe CLI."
    tail -f /dev/null
  fi
}

main() {
  start_stripe_service
}

main
