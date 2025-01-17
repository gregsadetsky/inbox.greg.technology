FROM python:3.12.1

RUN apt update -y
RUN apt-get install -y magic-wormhole

# docker will not re-pip install if requirements.txt doesn't change
WORKDIR /code
ADD ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

RUN sleep 10

ADD . /code

CMD ["python", "server.py"]
