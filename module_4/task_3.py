import unittest
from module_4.task_1 import app


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        app.config.update({
            'TESTING': True,
            'DEBUG': False,
            'WTF_CSRF_ENABLED': False
        })
        cls.client = app.test_client()
        cls.base_url: str = '/registration'

    def setUp(self) -> None:
        self.correct_test_data: dict = {
            "email": "testmail@mail.ru",
            "phone": "9216229566",
            "name": "Vadim",
            "address": "Street 13",
            "index": "602601",
            "comment": "Test request"
        }

    def test_full_email(self) -> None:
        self.correct_test_data.update({"email": "testmail@mail.ru"})
        self._checking_correctness_of_result("OK")

    def test_empty_email(self) -> None:
        self.correct_test_data.update({"email": None})
        self._checking_correctness_of_result("This field is required")

    def test_email_without_at_symbol(self) -> None:
        self.correct_test_data.update({"email": "testmailmail.ru"})
        self._checking_correctness_of_result("Invalid email address")

    def test_full_phone(self) -> None:
        self.correct_test_data.update({"phone": "9009009090"})
        self._checking_correctness_of_result("OK")

    def test_empty_phone(self) -> None:
        self.correct_test_data.update({"phone": None})
        self._checking_correctness_of_result("This field is required")

    def test_phone_length_is_differs_from_correct(self) -> None:
        self.correct_test_data.update({"phone": "9"})
        self._checking_correctness_of_result("Invalid length number")
        self.correct_test_data.update({"phone": "9"*11})
        self._checking_correctness_of_result("Invalid length number")

    def test_phone_is_not_number(self) -> None:
        self.correct_test_data.update({"phone": "8100asd100"})
        self._checking_correctness_of_result("Not a valid integer value")
    
    def test_full_name(self) -> None:
        self.correct_test_data.update({"name": "Oleg"})
        self._checking_correctness_of_result("OK")

    def test_empty_name(self) -> None:
        self.correct_test_data.update({"name": None})
        self._checking_correctness_of_result("This field is required")
    
    def test_full_address(self) -> None:
        self.correct_test_data.update({"address": "World"})
        self._checking_correctness_of_result("OK")

    def test_empty_address(self) -> None:
        self.correct_test_data.update({"address": None})
        self._checking_correctness_of_result("This field is required")
    
    def test_full_index(self) -> None:
        self.correct_test_data.update({"index": "602"})
        self._checking_correctness_of_result("OK")

    def test_empty_index(self) -> None:
        self.correct_test_data.update({"index": None})
        self._checking_correctness_of_result("This field is required")

    def test_index_is_not_number(self) -> None:
        self.correct_test_data.update({"phone": "1s1"})
        self._checking_correctness_of_result("Not a valid integer value")

    def test_full_comment(self) -> None:
        self.correct_test_data.update({"comment": "World"})
        self._checking_correctness_of_result("OK")
    
    def test_empty_comment(self) -> None:
        self.correct_test_data.update({"comment": None})
        self._checking_correctness_of_result("OK")

    def _checking_correctness_of_result(self, answer: str) -> None:
        response = self.client.post(self.base_url, data=self.correct_test_data)
        response_data = response.get_data(as_text=True)
        self.assertIn(answer, response_data)


if __name__ == '__main__':
    unittest.main()
