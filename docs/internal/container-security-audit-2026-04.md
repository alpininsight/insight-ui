# Container Security Audit — Insight UI Dockerfile (2026-04)

> Moved from `alpininsight/.github-private` so the active remediation record
> lives with the affected service in this repository.

**Repository:** `alpininsight/insight-ui`

**Title:** `feat(security): Add digest pinning and consider uv migration for Insight UI Dockerfile`

**Labels:** `security`, `dockerfile`, `enhancement`

---

## Summary
The Insight UI Dockerfile has solid production practices (multi-stage, non-root, HEALTHCHECK) but lacks base image digest pinning for supply-chain security and could benefit from migrating to `uv` for modern dependency management.

## Current State
```dockerfile
FROM python:3.13-slim AS builder
# ... wheel-based approach (solid but older pattern)
# Missing: digest pinning on base images
# Missing: uv for modern dependency resolution
```

Strengths:
- ✅ Multi-stage build (builder → runtime)
- ✅ Non-root user (app:app)
- ✅ HEALTHCHECK implemented
- ✅ Entrypoint script management
- ✅ Staticfiles collected

Gaps:
- ❌ No digest pinning on base images
- ⚠️ Using pip wheels instead of uv (less modern, but not critical)

## Desired State

### Option A (Minimal — Recommended for immediate fix)
Add digest pinning to both FROM statements.

### Option B (Enhanced — Recommended for long-term)
Migrate to uv + frozen dependencies for consistency with ecosystem standards (posidra-auth-factory, onto-3dwiz, tender-api).

## Proposed Changes

### Option A: Digest Pinning Only

```dockerfile
FROM python:3.13-slim@sha256:3d5ed973e45820f5ba5e46bd065bd88b3a504ff0724d85980dcd05eab361fcf4 AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /build

COPY requirements.txt .

RUN pip wheel --wheel-dir /wheels -r requirements.txt "uvicorn[standard]" gunicorn

FROM python:3.13-slim@sha256:3d5ed973e45820f5ba5e46bd065bd88b3a504ff0724d85980dcd05eab361fcf4 AS runtime

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
```

### Option B: uv Migration (Future Enhancement)

Convert `requirements.txt` to `pyproject.toml` + `uv.lock`:

```toml
[project]
name = "insight-ui"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    # Copy all from requirements.txt
    "django>=6.0",
    "uvicorn[standard]>=0.32",
    "gunicorn>=22.0",
    # ... etc
]
```

Then:
```bash
uv pip compile requirements.txt -o pyproject.toml
uv lock
```

Updated Dockerfile:
```dockerfile
FROM python:3.13-slim@sha256:3d5ed973e45820f5ba5e46bd065bd88b3a504ff0724d85980dcd05eab361fcf4 AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# ... rest of runtime stage same as current
```

## Acceptance Criteria
- [ ] Both FROM statements (builder and runtime) have digest pinning
- [ ] Build succeeds without errors
- [ ] No functional regressions in Insight UI
- [ ] Staticfiles collection works
- [ ] Kubernetes probes integrated (HEALTHCHECK already exists)

## Security & Reliability Impact
- **Supply-chain security:** Digest pinning prevents base image mutations
- **Build reproducibility:** Same digest ensures consistent builds
- **Future modernization:** uv option prepares for ecosystem-wide adoption

## Testing
```bash
docker build -t insight-ui:v2 .
docker run -d --name insight-ui-test insight-ui:v2
curl http://localhost:8000/
docker stop insight-ui-test
```

## Related
- Tracking: Platform-wide Dockerfile standardization
- Reference: posidra-auth-factory/Dockerfile, onto-3dwiz/Dockerfile
- Follow-up: Consider uv migration in future sprint for consistency
