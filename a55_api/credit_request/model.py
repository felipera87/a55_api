from datetime import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


from a55_api.extensions import db


class CreditRequest(db.Model):
    __tablename__ = 'credit_requests'

    id = db.Column(db.Integer, primary_key=True)

    amount_required = db.Column(db.Float())
    ticket = db.Column(UUID(as_uuid=True),
                       default=uuid4)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('users.id'),
                        nullable=False)
    status = db.Column(db.String(),
                       default="In Progress")

    created_at = db.Column(db.DateTime(),
                           nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(),
                           nullable=False,
                           default=datetime.utcnow)

    def __init__(self, amount_required, user_id):
        self.amount_required = amount_required
        self.user_id = user_id

    def __repr__(self):
        return f'CreditRequest(amount_required={self.amount_required}, user_id="{self.user_id}")'

    def __str__(self):
        return f"Credit request {self.status} of {self.amount_required} created at {self.created_at} (ticket: {self.ticket})"

    def save(self):
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
