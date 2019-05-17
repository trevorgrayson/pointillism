IMAGE := tgrayson/pointillism

compile:
	pip install -r requirements.txt

clean:
	find . -name "*.pyc" -delete

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
