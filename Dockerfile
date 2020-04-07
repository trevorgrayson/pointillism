FROM python:3.7-alpine

ENV HOST https://raw.githubusercontent.com 
ENV PYTHONPATH /app:$PYTHONPATH

EXPOSE 5001

RUN apk add --update graphviz ttf-freefont

COPY *.py /app/
COPY server /app/server
COPY renderer /app/renderer
COPY requirements.txt /
COPY public /srv/vhosts/pointillism/

RUN pip install -r requirements.txt

RUN ls /
ENTRYPOINT ["python"]
CMD ["-m", "server"]
