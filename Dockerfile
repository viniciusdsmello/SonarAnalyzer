FROM python:3.8.2-slim

WORKDIR /usr/app/src

COPY requirements.txt requirements.txt

RUN apt-get update \
	&& apt-get upgrade -y \
	&& apt-get -y install apt-utils gcc libpq-dev libsndfile-dev

RUN pip install -r requirements.txt

COPY src ./src
COPY docs ./docs

COPY main.py ./main.py

CMD ["sh", "-c", "streamlit run --server.port $PORT /usr/app/src/main.py"]
