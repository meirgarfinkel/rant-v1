.PHONY: install

install:
	@echo "Installing Python dependencies..."
	uv sync --frozen
	@echo "Installing Tailwind npm dependencies..."
	python manage.py tailwind install
	@echo "Collecting static files..."
	uv run manage.py collectstatic --noinput
	@echo "Starting Tailwind in watch mode..."
	python manage.py tailwind start &
	@echo "Migrating the db..."
	python manage.py migrate
	@echo "Starting Django development server..."
	uv run python manage.py runserver 0.0.0.0:8000
