FROM python:3.11.2-alpine

ENV LOGLEVEL=INFO
ENV TOKEN=
ENV PREFIX="?"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD python3 main.py --token=${TOKEN} --prefix=${PREFIX} --loglevel ${LOGLEVEL}