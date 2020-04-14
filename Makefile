IMAGE := tgrayson/pointillism
VERSION_NEW := $(shell ./bin/version_next)

FLASK_RUN_PORT?=5000
PYTHON := python3
VENV = .venv
VENV_BUILD = .venv.build
HOST ?= https://raw.githubusercontent.com
PROJECT=pointillism

export HOST
export FLASK_RUN_PORT
export GITHUB_CLIENT_ID
export GITHUB_SECRET
export PROJECT
export ENV=develop
export ADMIN_USER, ADMIN_PASS
export LDAP_HOST=ipsumllc.com
export PYTHONPATH=.:$(VENV):$(VENV_BUILD)

server: compile
	@test -n "$(HOST)" # set $$HOST variable
	$(PYTHON) -m server

compile: $(VENV)
$(VENV): requirements.txt requirements/app.txt
	$(PYTHON) -m pip install -t $(VENV) -r requirements.txt
	touch $(VENV)

compileAll: compile $(VENV_BUILD)
$(VENV_BUILD): requirements/build.txt
	$(PYTHON) -m pip install -t $(VENV) -r requirements/build.txt
	touch $(VENV_BUILD)
	
$(VENV): requirements.txt
	$(PYTHON) -m pip install -t $(VENV) -r requirements.txt
	touch $(VENV)

clean:
	find . -name "*.pyc" -delete
	rm -rf $(VENV) $(VENV_BUILD)
	# docker rm pointillism
	# docker rmi tgrayson/pointillism

image: 
	docker build -t $(IMAGE) .

imagePush: image
	echo "$(DOCKER_PASS)" | docker login -u "$(DOCKER_USER)" --password-stdin
	docker push $(IMAGE)

deploy:
	@# cat this into | ssh pointillism.io
	@echo "~/bin/deploy pointillism; $(shell paste -sd ';' ENV); docker run --name $(PROJECT) -e ADMIN_USER -e ADMIN_PASS -e LDAP_HOST -e GITHUB_SECRET -e GITHUB_CLIENT_ID -e PAYPAL_CLIENT_ID -d -p 5001:5001 --restart=always tgrayson/$(PROJECT):latest"

versionBump:
	git pull --tags
	git tag $(VERSION_NEW)
	git push --tags
test: compileAll
	$(PYTHON) -m pytest

integ: compileAll
	$(PYTHON) -s -m pytest -s test/models/*_integ.py

console:
	$(PYTHON) 

validate: test integ image

.PHONY: test
