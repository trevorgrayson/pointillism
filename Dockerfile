FROM python:latest

ENV HOST https://raw.githubusercontent.com 

EXPOSE 5001

RUN apt-get update && apt-get install -y graphviz

ADD *.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["server.py"]
