from a55_api.settings import MAX_AMOUNT, MAX_AGE


class Validator():

    def __init__(self, amount, age):
        self.amount = amount
        self.age = age

    def check_max_amount(self):
        return self.amount <= MAX_AMOUNT

    def check_max_age(self):
        return self.age >= MAX_AGE

    def validate(self):
        return all([
            self.check_max_amount(),
            self.check_max_age()
        ])
