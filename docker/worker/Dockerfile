FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8080

COPY . .
CMD ["celery", "-A", "a55_api.validator_worker.main:celery", "worker", "-l", "info"]