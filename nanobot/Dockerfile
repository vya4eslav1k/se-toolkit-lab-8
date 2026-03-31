# Simple Dockerfile for nanobot
# Build context is ./nanobot

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy nanobot project files
COPY pyproject.toml ./

# Sync dependencies (this will install nanobot-ai from URL)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project

# Copy the rest of the nanobot project
COPY . /app/nanobot/

# Install the nanobot package
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Install mcp-lms from the workspace mount
COPY --from=workspace mcp/mcp-lms /app/mcp/mcp-lms
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --editable /app/mcp/mcp-lms

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
