build:
	pip install -r requirements.txt

server:
	test -n "$(HOST)" # set $$HOST variable
	FLASK_APP=server.py flask run

clean:
	find . -name "*.pyc" -delete

deploy:
	# npm install serverless
	serverless deploy
