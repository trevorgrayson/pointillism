IMAGE := tgrayson/pointillism

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
	git tag `git tag -l v[0-9]* | sort | head -n1 |  awk '/v/{split($NF,v,/[.]/); $NF=v[1]"."v[2]"."++v[3]}1'`
	git push --tags
