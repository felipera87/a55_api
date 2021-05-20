from a55_api.user.model import User


class UserRepository(User):
    @classmethod
    def get_by_external_id(cls, user_id):
        return cls.query.filter_by(external_id=user_id).first()

    @classmethod
    def get_all_users(cls):
        return cls.query.all()
