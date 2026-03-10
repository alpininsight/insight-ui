FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /build

COPY requirements.txt .

RUN pip wheel --wheel-dir /wheels -r requirements.txt "uvicorn[standard]" gunicorn

FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV DEBUG=false
ENV IS_PROD=true
ENV RUN_MIGRATIONS=1
ENV RUN_COLLECTSTATIC=0

RUN addgroup --system app \
    && adduser --system --ingroup app app

WORKDIR /app

COPY --from=builder /wheels /wheels

RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* \
    && rm -rf /wheels

COPY --chown=app:app . /app
COPY --chown=app:app docker/entrypoint.sh /entrypoint.sh

RUN chmod 755 /entrypoint.sh \
    && mkdir -p /app/staticfiles \
    && python manage.py collectstatic --noinput \
    && python manage.py check \
    && chown -R app:app /app

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=5 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=2)" || exit 1

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "core.asgi:application"]
