from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Str(attribute="external_id")
    name = fields.Str()
    birth_date = fields.DateTime()


class CreateUserSchema(Schema):
    name = fields.Str(required=True)
    birth_date = fields.Date(required=True)


class UpdateUserSchema(Schema):
    name = fields.Str()
    birth_date = fields.Date()


user_schema = UserSchema()
user_schemas = UserSchema(many=True)
create_user_schema = CreateUserSchema()
update_user_schema = UpdateUserSchema()
