FROM python:3.11.2-alpine

ARG LOGLEVEL=DEBUG
ARG TOKEN=
ARG PREFIX="?"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "main.py", "--token=${TOKEN} --prefix=${PREFIX}" ]