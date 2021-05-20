from a55_api.credit_request.model import CreditRequest


class CreditRequestRepository(CreditRequest):
    @classmethod
    def get_by_ticket(cls, ticket):
        return cls.query.filter_by(ticket=ticket).first()

    @classmethod
    def get_all_requests(cls):
        return cls.query.all()
