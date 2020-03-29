IMAGE := tgrayson/pointillism
VERSION_NEW := $(shell ./bin/version_next)

FLASK_RUN_PORT?=5000
PYTHON := python
VENV = .venv

export FLASK_RUN_PORT
export PYTHONPATH=.:($VENV)

compile:
	$(PYTHON) -m pip install -t $(VENV) -r requirements.txt

clean:
	find . -name "*.pyc" -delete
	docker rm pointillism
	docker rmi tgrayson/pointillism

server:
	test -n "$(HOST)" # set $$HOST variable
	FLASK_APP=server.py flask run

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
