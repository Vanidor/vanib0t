FROM python:3.11.2-alpine

ENV LOGLEVEL=INFO
ENV TOKEN=
ENV PREFIX="?"
ENV OPENAI_API_KEY=
ENV DATABASE_PATH="settings/bot.sqlite"

ENV PICOSHARE_URL=

ENV CHATGPT_MAX_TOKENS=60
ENV CHATGPT_TEMPERATURE=1
ENV CHATGPT_N=1
ENV CHATGPT_TOP_P=1
ENV CHATGPT_PRESENCE_PENALTY=0
ENV CHATGPT_FREQUENCY_PENALTY=0
ENV CHATGPT_MAXIMUM_WORDS=30

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD python3 main.py --token=${TOKEN} --prefix=${PREFIX} --openai_api_key=${OPENAI_API_KEY} --loglevel ${LOGLEVEL} --database_path ${DATABASE_PATH} --chatgpt_max_tokens=${CHATGPT_MAX_TOKENS} --chatgpt_temperature=${CHATGPT_TEMPERATURE} --chatgpt_n=${CHATGPT_N} --chatgpt_top_p=${CHATGPT_TOP_P} --chatgpt_presence_penalty=${CHATGPT_PRESENCE_PENALTY} --chatgpt_frequency_penalty=${CHATGPT_FREQUENCY_PENALTY} --chatgpt_maximum_words=${CHATGPT_MAXIMUM_WORDS} --picoshare_url=${PICOSHARE_URL}