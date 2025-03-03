FROM python:3.12-bullseye

WORKDIR /code

COPY ./requirements.txt /code

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
