FROM python:3.7-alpine

ENV HOST https://raw.githubusercontent.com 

EXPOSE 5001

RUN apk add --update graphviz ttf-freefont

ADD *.py /
ADD requirements.txt /
ADD public /srv/vhosts/pointillism/

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["server.py"]
