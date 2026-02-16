FROM python:3.13-slim AS python

# Build requirements
FROM python AS python-build-stage

RUN apt-get update && apt-get install -y git && apt-get install --no-install-recommends -y

COPY ./requirements.txt .
RUN pip wheel --wheel-dir /usr/src/app/wheels -r requirements.txt "uvicorn[standard]" gunicorn

# The real container
FROM python AS python-run-stage

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN addgroup --system nonroot \
    && adduser --system --ingroup nonroot nonroot

RUN apt-get update && apt-get install --no-install-recommends -y \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Requirements from build stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

# Set directory
WORKDIR /app

# Copy files
COPY . .

# Copy environment file
COPY --chown=app:app .env.example /app/.env

# Run collectstatic
RUN python manage.py collectstatic --noinput

# Give permissions to nonroot user
RUN chown -R nonroot:nonroot /app

# Switch to 'nonroot'
USER nonroot

# Expose port
EXPOSE 8000

# Define healthcheck
HEALTHCHECK --interval=30s --timeout=3s CMD curl --silent --show-error --fail http://localhost:8000/ || exit 1

# Define start command
CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0", "core.asgi:application"]
