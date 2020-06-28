FROM tgrayson/build
FROM python:3.7-alpine

ENV HOST https://raw.githubusercontent.com 
ENV PYTHONPATH .:/:$PYTHONPATH
ENV THEME_DIR /themes
EXPOSE 5001

RUN apk add --update graphviz ttf-freefont build-base openldap-dev python2-dev python3-dev


COPY *.py /
COPY point /point
COPY ldapauth /ldapauth
COPY requirements.txt /
COPY requirements /requirements
COPY public /srv/vhosts/pointillism/
COPY themes /themes
COPY plantuml.jar /

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["-m", "point.server"]
