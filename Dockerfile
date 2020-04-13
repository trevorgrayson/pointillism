FROM python:3.7-alpine

ENV HOST https://raw.githubusercontent.com 
ENV PYTHONPATH .:/:$PYTHONPATH

EXPOSE 5001

RUN apk add --update graphviz ttf-freefont build-base openldap-dev python2-dev python3-dev


COPY *.py /
COPY server /server
COPY ldapauth /ldapauth
COPY renderer /renderer
COPY models /models
COPY requirements.txt /
COPY requirements /requirements
COPY public /srv/vhosts/pointillism/

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["-m", "server"]
