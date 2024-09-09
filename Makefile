mig:
	python manage.py makemigrations
	python manage.py migrate

clean:
	isort --settings-file ./.isort.cfg .
	flake8 --config .flake8 .

remove_migration:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete

run:
	docker start commerce
	./manage.py runserver

init:
	/init-db.sh
