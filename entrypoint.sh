#!/bin/bash
set -e

echo "APP_ENV is set to ${APP_ENV}"

# Run environment-specific logic
if [ "$APP_ENV" = "development" ]; then
    # Development: Run Tailwind in watch mode and apply migrations
    echo "Starting Tailwind in watch mode..."
    uv run python manage.py tailwind start &  # Runs in background

    echo "Running migrations..."
    uv run python manage.py migrate

    echo "Collecting static files..."
    uv run python manage.py collectstatic --noinput

    echo "Starting Gunicorn in development mode..."
    exec uv run gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 4 --reload --timeout 120

elif [ "$APP_ENV" = "production" ]; then
    # Production: Build the Tailwind CSS and then use Gunicorn
    echo "Building Tailwind CSS..."
    uv run python manage.py tailwind build  # Builds and minifies the CSS

    echo "Running migrations..."
    uv run python manage.py migrate

    echo "Collecting static files..."
    uv run python manage.py collectstatic --noinput

    echo "Starting Gunicorn in production mode..."
    exec uv run gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120

else
    echo "Error: APP_ENV is not set to either 'development' or 'production'."
    exit 1
fi
