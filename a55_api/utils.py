import logging
from uuid import UUID


def validate_uuid(uuid):
    try:
        UUID(uuid)
        return True
    except ValueError:
        return False


LOG_FORMAT = "[%(asctime)s: %(module)s %(funcName)s] %(message)s"
log = logging
log.basicConfig(level=log.INFO, format=LOG_FORMAT)
