FROM python:3.10

COPY . ./signals
WORKDIR ./signals

RUN pip install -r requirements.txt

CMD gunicorn -b 0.0.0.0:8000 app:server
