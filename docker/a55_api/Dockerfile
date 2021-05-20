FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8080

COPY . .

CMD ["/bin/sh", "-c", "waitress-serve --call a55_api.app:create_app"]