from tests.test_base import BaseTest
from a55_api.utils import validate_uuid


class UtilsTest(BaseTest):
    def test_invalid_uuid(self):
        messed_up_uuid = 'dfjfsdkfjs'
        check_result = validate_uuid(messed_up_uuid)

        self.assertFalse(check_result)

    def test_valid_uuid(self):
        valid_uuid = 'c10d5842-5562-47d9-8d2c-b00c0e22086a'
        check_result = validate_uuid(valid_uuid)

        self.assertTrue(check_result)
