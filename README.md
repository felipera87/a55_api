# a55_api

The a55_api is an application for a technical evaluation, the proposal is to solve a simple problem with a REST API and using asynchronous processing for validation. It was built with Flask, but many other third-party tools were used to accomplish this.

## Problem specs

- The user can open a credit request using a POST request, it must return a ticket for a future query.
- The user can check the credit request state with the ticket using a GET request (Approved or Rejected)
- Validations must be asynchronous and must check for amount lesser than R$ 100.000,00 and age higher than 18 years.

## How to run this project

### Option 1: Run the containers manually (better for development)

For this option to work you need a Python environment already configured and all the requirements installed:

```sh
$ pip install -r requirements.txt

# for tests and development
$ pip install -r dev-requirements.txt
```

#### Prepare the database

1. Build and run the Postgres database:

```sh
$ docker build -t a55-postgres-image ./database
$ docker run -d --rm --name a55-postgres -p 5432:5432 a55-postgres-image

# stop it for a fresh database
$ sudo docker stop a55-postgres
```

2. Run the migrations (it will build based on the models):

If `migrations` folder don't exist:

```sh
$ export FLASK_APP=run_app.py
$ flask db init
$ flask db migrate -m "Initial migration."
```

Otherwise just upgrade de database:

```sh
$ export FLASK_APP=run_app.py
$ flask db upgrade
```

#### Start async workers

1. Start the Redis service:

```sh
$ docker run --rm -p 6379:6379 -d redis
```

2. Open another terminal and start a celery worker:

```sh
$ celery -A a55_api.validator_worker.main:celery worker -l info
```

#### Start the Flask API

You can do this on two ways, run a debug app or something similar to production.
For a debug session:

```sh
$ export FLASK_APP=run_app.py
$ export FLASK_DEBUG=1
$ flask run
```

Running the container:

```sh
$ docker build . -t a55_api -f ./docker/a55_api/Dockerfile
$ docker run --rm -p 5000:8080 a55_api
```

### Option 2: Run the composer (good for a quick setup)

Make sure the migrations folder exists and run the `docker-compose` file:

```sh
$ docker-compose up

# alternatively you may want to start fresh containers
$ docker-compose up --force-recreate --renew-anon-volumes
```

To bring it down:

```sh
$ docker-compose down

# alternatively you may want to remove images to rebuild the Dockerfile
$ docker-compose down --rmi all
```

It may take a while to run the migration service on this `docker-compose` file. I've put it there just for the convenience but ideally it should be on a CI script.

## How to run tests

You need to prepare the database first with the migrations (check "Prepare the database" section). You can run the `unittest` module or use `coverage` for a report:

```sh
# unittest in action
$ python -m unittest discover -v -s tests

# coverage reports (need to install dev-requirements)
$ coverage run --source=a55_api -m unittest discover -v -s tests
$ coverage report -m
```

## Endpoints documentation

I was going to set a swagger doc, but time is short and the deadline is here, I'll try to set it up today but for now I'll just list the endpoints:

- `GET /user`: list all users
- `GET /user/<id>`: get specified user
- `DELETE /user/<id>`: delete specified user
- `POST /user`: create one user

```json
{
  "name": "test",
  "birth_date": "2001-01-01"
}
```

- `PUT /user`: update one user

```json
{
  "name": "test2",
  "birth_date": "2001-01-02"
}
```

- `GET /credit_request/<ticket>`: check credit request status by ticket
- `GET /credit_request`: list all credit request status
- `POST /credit_request`: request credit

```json
{
  "amount_required": 5000,
  "user_id": "<valid user id>"
}
```

Some endpoints may seem strange (list all credit requests?) but it's just for convenience, to make it easier to see the data.
