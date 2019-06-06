IMAGE := tgrayson/pointillism
VERSION_NEW := $(shell ./bin/version_next)

compile:
	pip install -r requirements.txt

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
	git tag $(VERSION_NEW)
	git push --tags
