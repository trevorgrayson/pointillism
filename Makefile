include Makefile.admin
IMAGE := tgrayson/pointillism
VERSION_NEW := $(shell ./bin/version_next)

FLASK_RUN_PORT?=5000
PYTHON:=python3
VENV=.venv
VENV_BUILD=.venv.build
DEPLOY_HOST?=pointillism.io
HOST?=https://raw.githubusercontent.com
TEST_HOST?=http://staging.pointillism.io
TEST?=test
PROJECT=pointillism
ADMIN_USER?=admin@ipsumllc.com
ADMIN_PASS?=tugboat
VERSION_NEW := ${shell git tag -l v[0-9]* | sort -V -r | head -n1 |  awk '/v/{split($$NF,v,/[.]/); $$NF=v[1]"."v[2]"."++v[3]}1'}
PLANT_JAR?=plantuml.jar

export ENV=develop
export HOST
export DEPLOY_HOST
export FLASK_RUN_PORT
export GITHUB_CLIENT_ID
export GITHUB_SECRET
export PROJECT
export ADMIN_USER, ADMIN_PASS
export LDAP_HOST=ldap.pointillism.io
export PYTHONPATH=.:$(VENV):$(VENV_BUILD)
export PAYPAL_CLIENT_ID
export AIRBRAKE_PROJECT_ID
export AIRBRAKE_API_KEY
export LOG
export PLANT_JAR

.EXPORT_ALL_VARIABLES:
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
	# docker rmi pointillism/pointillism

package: compile
	cd react && make -f Makefile package

image: package 
	docker build -t $(IMAGE) .

imagePush: image # versionBump
	echo "$(DOCKER_PASS)" | docker login -u "$(DOCKER_USER)" --password-stdin
	docker push $(IMAGE)

imageTest:
	@docker stop pointillism && docker rm pointillism || echo "pointillism not running."
	@docker run --name $(PROJECT) --env-file ENV -d -p 5001:5001 --restart=always $(IMAGE):latest

deploy:
	cat ./bin/deploy.remote.sh | ssh $(DEPLOY_HOST)
	TEST_HOST=https://pointillism.io GIT_TOKEN=123 make smoke

versionBump:
	@git pull --tags
	@git tag $(VERSION_NEW)
	@git push --tags
	@echo "tagged $(VERSION_NEW)"

test: compileAll
	$(PYTHON) -m pytest -s --cov=point $(TEST)

integ: compileAll
	$(PYTHON) -s -m pytest -s -c pytest.integ.ini $(TEST)

lint:
	$(PYTHON) -m pyflakes point
	$(PYTHON) -m pycodestyle point

lintAuto:
	$(PYTHON) -m yapf --recursive -i `find point`

console:
	$(PYTHON) 

smoke:
	$(PYTHON) -m pytest test/smoke/mvp_smoke.py

status:
	$(PYTHON) -m status

legal: legal/privacy.md legal/terms.md
	pandoc -f markdown -t html5 -o point/server/static/privacy.html legal/privacy.md 
	pandoc -f markdown -t html5 -o point/server/static/terms.html legal/terms.md 
	pandoc -f markdown -t html5 -o point/server/static/do-not-sell.html legal/do-not-sell.md 
	pandoc -f markdown -t html5 -o react/public/privacy.html legal/privacy.md 
	pandoc -f markdown -t html5 -o react/public/terms.html legal/terms.md 
	pandoc -f markdown -t html5 -o react/public/do-not-sell.html legal/do-not-sell.md 
	
	touch legal
	# -c style.css

validate: test integ image

.PHONY: test legal status
