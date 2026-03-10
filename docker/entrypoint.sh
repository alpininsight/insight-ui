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

exec "$@"
