# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/app`
WORKDIR /app

# Ensure the UV binary is on the PATH
ENV PATH="/root/.local/bin:$PATH"

# Set environment variables for Python and UV
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1

# Install system dependencies and clean up apt caches
RUN apt-get update && apt-get install -y --no-install-recommends \
    git bash build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Create a group with GID 1000
RUN groupadd --gid 1000 docker

# Create a non-root user with UID 1000, GID 1000, and /app as the home directory
RUN useradd --uid 1000 --gid 1000 --no-create-home --home /app --shell /bin/bash docker

# Copy the project files into the image (including pyproject.toml)
COPY . /app

# Use BuildKit caching to install and lock dependencies using UV.
# Mount cache for UV and create lockfile then install dependencies
RUN --mount=type=cache,target=/app/.cache/uv \
    uv lock && uv sync --frozen

# Collect static files for Django (adjust/manage if needed)
RUN uv run manage.py collectstatic --noinput

# Change ownership of /app to the non-root user
RUN chown -R docker:docker /app

# Switch to non-root user
USER docker

# Expose the port that Gunicorn will run on
EXPOSE 8000

# Run the Django application using Gunicorn
CMD ["uv", "run", "gunicorn", "-b", ":8000", "app.wsgi:application"]
