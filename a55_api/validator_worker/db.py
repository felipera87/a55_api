from sqlalchemy import create_engine, text

from a55_api.settings import DB_NAME, DB_PASS, DB_SERVER, DB_USER, DB_PORT

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_SERVER}:{DB_PORT}/{DB_NAME}")


def update_credit_request_status(ticket, status):
    with engine.connect() as connection:
        connection.execute(
            text(
                f"update credit_requests set status = '{status}' where ticket = '{ticket}'")
        )
