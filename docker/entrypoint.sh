#!/bin/sh
set -eu

is_truthy() {
    value=$(printf '%s' "${1:-}" | tr '[:upper:]' '[:lower:]')
    case "$value" in
        1|true|yes|on)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

run_manage_command() {
    echo "==> python manage.py $*"
    python manage.py "$@"
}

if is_truthy "${RUN_MIGRATIONS:-1}"; then
    run_manage_command migrate --noinput
fi

if is_truthy "${RUN_COLLECTSTATIC:-0}"; then
    run_manage_command collectstatic --noinput
fi

if [ "${1:-}" = "gunicorn" ]; then
    gunicorn_cmd_args="${GUNICORN_CMD_ARGS:-}"

    if [ -n "${SERVER_LOG_LEVEL:-}" ]; then
        normalized_server_log_level=$(printf '%s' "${SERVER_LOG_LEVEL}" | tr '[:upper:]' '[:lower:]')
        gunicorn_cmd_args="${gunicorn_cmd_args} --log-level ${normalized_server_log_level}"
    fi

    if is_truthy "${ACCESS_LOG_ENABLED:-0}"; then
        gunicorn_cmd_args="${gunicorn_cmd_args} --access-logfile -"
    fi

    export GUNICORN_CMD_ARGS="${gunicorn_cmd_args# }"
fi

exec "$@"
