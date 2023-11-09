FROM python:3.10.0-alpine

RUN apk add --no-cache --virtual .build-deps gcc postgresql-dev musl-dev python3-dev ca-certificates
RUN apk add libpq

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN apk del --no-cache .build-deps

RUN mkdir -p /code
COPY main.py /code/
COPY models /code/models
COPY tests /code/tests
COPY utils /code/utils
COPY api /code/api
RUN mkdir -p /code/logs
WORKDIR /code
EXPOSE 8080

ENTRYPOINT [ "python", "main.py" ]
