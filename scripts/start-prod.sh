set -e

DEFAULT_MODULE_NAME=src.main

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

DEFAULT_HYPERCORN_CONF=/src/hypercorn/hypercorn_conf.py
export HYPERCORN_CONF=${HYPERCORN_CONF:-$DEFAULT_HYPERCORN_CONF}
export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

# Start Gunicorn
hypercorn --forwarded-allow-ips "*" -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE"
