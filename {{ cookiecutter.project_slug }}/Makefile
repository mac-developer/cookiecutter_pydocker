help:
	@echo "docker-run - Delete docker container and recreate it"
	@echo "docker-build - Delete docker image and container. Image will be rebuild."


docker-run:
	docker rm -f {{ cookiecutter.docker_container }}
	docker run --name {{ cookiecutter.docker_container }} -v `pwd`:/usr/src/app -it {{ cookiecutter.docker_image }} bash

docker-build:
	docker rmi -f {{ cookiecutter.docker_image }}
	docker build -t {{ cookiecutter.docker_image }} .

clean-pyc:
	@find . -name '*.pyc' -exec rm -rf {} +
	@find . -name '__pycache__' -exec rm -rf {} +

clean-build:
	@find . -name '.cache' -exec rm -rf {} +
	@find . -name 'dist' -exec rm -rf {} +
	@find . -name 'build' -exec rm -rf {} +
	@find . -name '.isort.cfg' -exec rm -rf {} +
	@find . -name '.coverage' -exec rm -rf {} +
	@find . -name '.eggs' -exec rm -rf {} +
	@find . -name '*.egg-info' -exec rm -rf {} +

clean-logs:
	@find . -name '*.log' -exec rm -rf {} +
	@find . -name '*.log.*' -exec rm -rf {} +

clean: clean-build clean-pyc clean-logs
	@find . -name .DS_Store -exec rm -rf {} +

develop: clean
	pip install --upgrade pip
	pip install --no-cache-dir --use-wheel -r test-requirements.txt -e . > /dev/null

test: develop
	@pytest -vv --flake8 --cov="{{ cookiecutter.project_slug }}"
