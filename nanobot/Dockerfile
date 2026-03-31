# Dockerfile for nanobot with webchat support
# Build context is ./nanobot with workspace additional_context

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy workspace root pyproject.toml and uv.lock for dependency resolution
COPY --from=workspace . /app/

# Sync dependencies for nanobot project
RUN --mount=type=cache,target=/root/.cache/uv \
    cd /app/nanobot && uv sync --no-dev

# Install additional workspace packages (mcp-lms, webchat)
RUN --mount=type=cache,target=/root/.cache/uv \
    cd /app/nanobot && uv add mcp-lms nanobot-webchat mcp-webchat

# ---
# Stage 2: runtime image
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy the application from the builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

USER nonroot
WORKDIR /app/nanobot

CMD ["python", "/app/nanobot/entrypoint.py"]
