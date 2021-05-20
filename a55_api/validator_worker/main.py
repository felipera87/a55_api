import time
from celery import Celery

from a55_api.settings import REDIS_URL, WORKER_SIMULATED_TIME
from a55_api.utils import log

from a55_api.validator_worker.validator import Validator
from a55_api.validator_worker.db import update_credit_request_status

celery = Celery("tasks", broker=REDIS_URL)


@celery.task
def validate_credit_request(amount, ticket, age, wait_time=None):
    log.info(f"Worker validating ticket {ticket}: age {age} amount {amount}")
    # simulate a time consuming task
    if wait_time is None:
        wait_time = int(WORKER_SIMULATED_TIME)

    if wait_time > 0:
        time.sleep(wait_time)

    validator = Validator(amount, age)
    status = "Approved" if validator.validate() else "Denied"

    log.info(f"Setting {status} for ticket {ticket}")
    update_credit_request_status(ticket, status)

    log.info("Worker successfully validated")
    return status
