FROM python:3.14-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

ARG ARTIFACT_VERSION=0.0.0
ARG GIT_COMMIT_SHA=unknown
ARG BUILD_CREATED=unknown

WORKDIR /build

COPY requirements.txt .

RUN pip wheel --wheel-dir /wheels -r requirements.txt "uvicorn[standard]" gunicorn

FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV DEBUG=false
ENV IS_PROD=true
ENV SERVICE_NAMESPACE=alpininsight
ENV SERVICE_NAME=insight-ui
ENV PLATFORM_NAMESPACE=demo
ENV DEPLOYMENT_ENVIRONMENT=local
ENV DEPLOYMENT_LANE=
ENV DEPLOYMENT_SLOT=
ENV PUBLIC_BASE_URL=http://localhost:8000
ENV LOG_LEVEL=WARNING
ENV APP_LOG_LEVEL=INFO
ENV DJANGO_LOG_LEVEL=WARNING
ENV SERVER_LOG_LEVEL=WARNING
ENV ACCESS_LOG_ENABLED=0
ENV LOG_FORMAT=json
ENV RUN_MIGRATIONS=1
ENV RUN_COLLECTSTATIC=0

ARG ARTIFACT_VERSION=0.0.0
ARG GIT_COMMIT_SHA=unknown
ARG BUILD_CREATED=unknown

ENV ARTIFACT_VERSION=${ARTIFACT_VERSION}
ENV GIT_COMMIT_SHA=${GIT_COMMIT_SHA}

LABEL org.opencontainers.image.title="insight-ui" \
      org.opencontainers.image.source="https://github.com/alpininsight/insight-ui" \
      org.opencontainers.image.version="${ARTIFACT_VERSION}" \
      org.opencontainers.image.revision="${GIT_COMMIT_SHA}" \
      org.opencontainers.image.created="${BUILD_CREATED}"

ENV HOME=/home/app

RUN addgroup --system app \
    && adduser --system --home /home/app --ingroup app app

WORKDIR /app

COPY --from=builder /wheels /wheels

RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* \
    && rm -rf /wheels \
    && python -m pip uninstall --yes pip

COPY --chown=app:app . /app
COPY --chown=app:app docker/entrypoint.sh /entrypoint.sh

RUN chmod 755 /entrypoint.sh \
    && apt-get update \
    && apt-get install -y --no-install-recommends gettext \
    && mkdir -p /home/app \
    && mkdir -p /app/staticfiles \
    && SECRET_KEY="$(python -c "import secrets; print(secrets.token_urlsafe(64))")" python manage.py compilemessages --locale de --verbosity 0 \
    && SECRET_KEY="$(python -c "import secrets; print(secrets.token_urlsafe(64))")" python manage.py collectstatic --noinput \
    && SECRET_KEY="$(python -c "import secrets; print(secrets.token_urlsafe(64))")" python manage.py check \
    && apt-get purge -y --auto-remove gettext \
    && rm -rf /var/lib/apt/lists/* \
    && chown -R app:app /app /home/app

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=5 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2)" || exit 1

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "core.asgi:application"]
