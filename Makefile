include .env

env_file = --env-file .env

help:
	@echo "Makefile commands:"
	@echo "stop"
	@echo "restart"
	@echo "destroy"
build:
	docker-compose -f docker-compose.yml build -d $(c)
	docker-compose -f docker-compose.yml up -d $(c)
launch_broker:
	docker-compose --profile broker -f docker-compose.yml build -d $(c)
	docker-compose --profile broker -f docker-compose.yml up -d $(c)
launch_mailhog:
	docker-compose --profile mailhog -f docker-compose.yml build -d $(c)
	docker-compose --profile mailhog -f docker-compose.yml up -d $(c)
stop:
	docker-compose -f docker-compose.yml stop $(c)
restart:
	docker-compose -f docker-compose.yml stop $(c)
	docker-compose -f docker-compose.yml up -d $(c)
destroy:
	docker system prune -f --volumes $(c)
