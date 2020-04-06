IMAGE := tgrayson/pointillism
VERSION_NEW := $(shell ./bin/version_next)

FLASK_RUN_PORT?=5000
PYTHON := python3
VENV = .venv
HOST ?= https://raw.githubusercontent.com

export HOST
export FLASK_RUN_PORT
export PYTHONPATH=.:$(VENV)

server: compile
	@test -n "$(HOST)" # set $$HOST variable
	$(PYTHON) -m server

compile: $(VENV)
$(VENV): requirements.txt
	$(PYTHON) -m pip install -t $(VENV) -r requirements.txt
	touch $(VENV)

clean:
	find . -name "*.pyc" -delete
	# docker rm pointillism
	# docker rmi tgrayson/pointillism

image: 
	docker build -t $(IMAGE) .

imagePush:
	echo "$(DOCKER_PASS)" | docker login -u "$(DOCKER_USER)" --password-stdin
	docker push $(IMAGE)

deploy:
	# npm install serverless
	serverless deploy

versionBump:
	git pull --tags
	git tag $(VERSION_NEW)
	git push --tags
