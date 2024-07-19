mig:
	python manage.py makemigrations
	python manage.py migrate

remove_migration:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
