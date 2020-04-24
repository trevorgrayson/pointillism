IMAGE := tgrayson/pointillism
VERSION_NEW := $(shell ./bin/version_next)

FLASK_RUN_PORT?=5000
PYTHON := python3
VENV = .venv
VENV_BUILD = .venv.build
HOST ?= https://raw.githubusercontent.com
TEST_HOST ?= http://localhost:5001
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
	$(PYTHON) -m point.server

compile: $(VENV)
$(VENV): requirements.txt requirements/app.txt
	$(PYTHON) -m pip install -t $(VENV) -r requirements.txt
	touch $(VENV)

compileAll: compile $(VENV_BUILD)
$(VENV_BUILD): requirements/build.txt
	$(PYTHON) -m pip install -t $(VENV) -r requirements/build.txt
	touch $(VENV_BUILD)

clean:
	find . -name "*.pyc" -delete
	rm -rf $(VENV) $(VENV_BUILD)
	# docker rm pointillism
	# docker rmi tgrayson/pointillism

image: 
	# cd react && make -f Makefile package
	docker build -t $(IMAGE) .

imagePush: image
	echo "$(DOCKER_PASS)" | docker login -u "$(DOCKER_USER)" --password-stdin
	docker push $(IMAGE)

imageTest: image
	@docker stop pointillism && docker rm pointillism || echo "pointillism not running."
	@docker run --name $(PROJECT) --env-file ENV -d -p 5001:5001 --restart=always tgrayson/$(PROJECT):latest

deploy:
	./bin/deploy 

versionBump:
	git pull --tags
	git tag $(VERSION_NEW)
	git push --tags
test: compileAll
	$(PYTHON) -m pytest --cov=point

integ: compileAll
	$(PYTHON) -s -m pytest -s test/models/*_integ.py

console:
	$(PYTHON) 

smoke:
	$(PYTHON) -m pytest test/smoke/mvp_smoke.py

validate: test integ image

.PHONY: test
