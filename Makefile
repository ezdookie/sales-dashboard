first-start:
	make stop
	make remove
	make build
	make up
	sleep 10
	make init
	make vmin-sync
	make initial-subscriptions

init:
	make migrate
	make seeds

build:
	docker-compose build

up:
	docker-compose up -d

restart:
	make stop
	make up

stop:
	docker-compose stop

remove:
	docker-compose rm -f
	sudo rm -rf pgdata
	sudo rm -rf rddata

rebuild:
	make stop
	make build
	make up

resetdb:
	docker-compose exec web python manage.py flush --no-input
	make migrate
	make seeds

makemigrations:
	docker-compose exec web python manage.py makemigrations

migrate:
	docker-compose exec web python manage.py migrate

seeds:
	docker-compose exec web python manage.py loaddata base
	docker-compose exec web python manage.py loaddata initial_users
	docker-compose exec web python manage.py loaddata services
	make setup-users

initial-subscriptions:
	docker-compose exec web python manage.py loaddata initial_subscriptions
	make setup-permissions

shell:
	docker-compose exec web python manage.py shell

web-logs:
	docker-compose logs -f web

worker-logs:
	docker-compose logs -f worker

worker-restart:
	docker-compose restart worker
	make worker-logs

vmin-sync:
	docker-compose exec web python manage.py vminsync

setup-users:
	docker-compose exec web python manage.py setup_users

setup-permissions:
	docker-compose exec web python manage.py setup_permissions
