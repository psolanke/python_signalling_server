FROM ubuntu:16.04

#RUN apt-get update
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

#ENTRYPOINT [ "python" ]

CMD [ "gunicorn", "--worker-class", "eventlet", "-w", "1", "--log-file=-", "main_app:app" ]
