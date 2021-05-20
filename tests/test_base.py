from unittest import TestCase

from a55_api.app import create_app
from a55_api.extensions import db
from a55_api.settings import TestConfig


class BaseTest(TestCase):
    flask_app = create_app(TestConfig)

    def setUp(self):
        self.flask_app.app_context().push()

    def tearDown(self):
        with self.flask_app.app_context():
            db.session.remove()
