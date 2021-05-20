from marshmallow import Schema, fields


class CreditRequestSchema(Schema):
    id = fields.Str(attribute="external_id")
    amount_required = fields.Float()
    ticket = fields.Str()
    status = fields.Str()


class CreateCreditRequestSchema(Schema):
    amount_required = fields.Float(required=True)
    user_id = fields.Str(required=True)


credit_request_schema = CreditRequestSchema()
credit_request_schemas = CreditRequestSchema(many=True)
create_credit_request_schema = CreateCreditRequestSchema()
