# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set the working directory
WORKDIR /app

# Set Python environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git bash build-essential libpq-dev python3-pip nodejs npm && \
    rm -rf /var/lib/apt/lists/*

# Ensure pip is installed/upgraded
RUN python -m ensurepip --upgrade && python -m pip install --upgrade pip

# Create a custom home directory and a non-root user "docker" with UID/GID 1000
RUN mkdir -p /home && \
    groupadd --gid 1000 docker && \
    useradd --uid 1000 --gid 1000 --create-home --home-dir /home/docker --shell /bin/bash docker

# Copy the project files into the image
COPY . /app

# Use uv to install Python dependencies from pyproject.toml
RUN --mount=type=cache,target=/app/.cache/uv \
    uv lock && uv sync --no-group dev --frozen

# Copy the entrypoint script into the image and mark it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Change ownership of /app so that the non-root user can access it
RUN chown -R docker:docker /app

# Switch to the non-root user
USER docker

# Expose port 8000
EXPOSE 8000

# Use the entrypoint script to start processes
ENTRYPOINT ["/app/entrypoint.sh"]
