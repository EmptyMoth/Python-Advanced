import unittest
from module_5.task_2.task_2 import app


class TestRemotePythonCode(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        app.config.update({
            'TESTING': True,
            'DEBUG': False,
            'WTF_CSRF_ENABLED': False
        })

        cls.client = app.test_client()
        cls.base_url: str = '/python'

    def setUp(self) -> None:
        self.correct_test_data: dict = {
            "code": "print(\"Hello World!\")",
            "timeout": 5
        }

    def test_empty_code(self) -> None:
        self.correct_test_data.update({"code": None})
        response_data = self._get_response_data(self.correct_test_data)
        self.assertIn("This field is required", response_data)

    def test_timeout_out_of_range(self) -> None:
        self.correct_test_data.update({"timeout": -1})
        with self.subTest(data=self.correct_test_data):
            response_data = self._get_response_data(self.correct_test_data)
            self.assertIn("Number must be between", response_data)

        self.correct_test_data.update({"timeout": 50})
        with self.subTest(data=self.correct_test_data):
            response_data = self._get_response_data(self.correct_test_data)
            self.assertIn("Number must be between", response_data)

    def test_code_timeout(self) -> None:
        self.correct_test_data.update({"code": "import time \ntime.sleep(1000000)"})
        response_data = self._get_response_data(self.correct_test_data)
        self.assertIn("Программа не уложилась в поставленное время", response_data)

    def test_correct_code(self) -> None:
        self.correct_test_data.update({"code": "a=5-4 \nb=101 \nprint(102)"})
        response_data = self._get_response_data(self.correct_test_data)
        self.assertIn("102", response_data)

    def test_incorrect_code(self) -> None:
        self.correct_test_data.update({"code": 'print()"; echo "hacked'})
        response_data = self._get_response_data(self.correct_test_data)
        self.assertEqual("", response_data)

    def test_unsafe_code(self) -> None:
        self.correct_test_data.update({"code": "from subprocess import run\nrun(['./kill_the_system.sh'])"})
        response_data = self._get_response_data(self.correct_test_data)
        self.assertEqual("", response_data)

    def _get_response_data(self, data: dict) -> str:
        response = self.client.post(self.base_url, data=data)
        response_data = response.get_data(as_text=True)
        return response_data


if __name__ == '__main__':
    unittest.main()
