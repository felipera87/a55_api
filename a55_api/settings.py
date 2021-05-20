import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "example")
DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost")

# used to simulate a time consuming task for the worker, time in seconds
WORKER_SIMULATED_TIME = os.getenv("WORKER_SIMULATED_TIME", "5")

# validation parameters
MAX_AMOUNT = 100000
MAX_AGE = 18


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    ENV = "Production"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"postgresql://{DB_USER}:{DB_PASS}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
    )
    CELERY_BROKER_URL = REDIS_URL
    DEBUG = False


class DevConfig(Config):
    ENV = "Development"
    DEBUG = True
    CELERY_BROKER_URL = REDIS_URL
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


class TestConfig(Config):
    ENV = "Test"
    DEBUG = True
    CELERY_BROKER_URL = REDIS_URL
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
