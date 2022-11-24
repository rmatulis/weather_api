FROM python:3.9.15-slim

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app.py app.py

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "app:app"]