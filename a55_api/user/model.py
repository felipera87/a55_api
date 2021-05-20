from datetime import datetime, date
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from a55_api.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(UUID(as_uuid=True),
                            default=uuid4)

    name = db.Column(db.String())
    birth_date = db.Column(db.DateTime())

    credit_requests = db.relationship("CreditRequest",
                                      backref=db.backref("users", lazy=True))

    created_at = db.Column(db.DateTime(),
                           nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(),
                           nullable=False,
                           default=datetime.utcnow)

    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date

    def __repr__(self):
        return f'User(name="{self.name}", birth_date="{self.birth_date}")'

    def __str__(self):
        return f"User {self.name} created at {self.created_at} (external_id: {self.external_id})"

    def save(self):
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
