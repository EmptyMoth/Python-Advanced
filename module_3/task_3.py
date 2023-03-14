import unittest
from module_2.task_7 import app, get_storage_value


class MyTestCase(unittest.TestCase):
    app = None
    start_data: dict = {
        "20030823": [100, 200, 300],
        "20030832": [0],
        "20031023": [400],
        "20230314": [500],
    }

    @classmethod
    def setUpClass(cls) -> None:
        app.config['TESTING'] = True
        app.config['DEBAG'] = False
        cls.app = app.test_client()
        cls._fill_storage_with_initial_data()

    @classmethod
    def _fill_storage_with_initial_data(cls) -> None:
        base_url: str = "/add"
        for data, values in cls.start_data.items():
            for value in values:
                url: str = '/'.join([base_url, data, str(value)])
                cls.app.get(url)

    def test_correct_add_value(self) -> None:
        for date, values in self.start_data.items():
            with self.subTest(date=date, values=values):
                answer: int = sum(values)
                result: int = get_storage_value(date)
                self.assertEqual(result, answer)

    def test_add_does_not_accepts_incorrect_format(self) -> None:
        incorrect_format: [str] = ["/add/map 23 2000/100", "/add/2000.03.23/100", "/add/00323/100"]
        for format in incorrect_format:
            with self.subTest(format=format):
                with self.assertRaises((TypeError, ValueError)):
                    self.app.get(format)

    def test_correct_calculate_for_year_with_one_month(self) -> None:
        self._test_correct_calculate_for_year("2023", "500")

    def test_correct_calculate_for_year_with_many_month(self) -> None:
        self._test_correct_calculate_for_year("2003", "1000")

    def test_correct_calculate_for_missing_year(self) -> None:
        answer: str = "Empty"
        url: str = '/'.join(["/calculate", "1900"])
        response = self.app.get(url)
        result: str = response.data.decode()
        self.assertEqual(result, answer)

    def test_correct_calculate_for_month_with_one_month(self) -> None:
        self._test_correct_calculate_for_month("2023", "3", "500")

    def test_correct_calculate_for_month_with_many_month(self) -> None:
        self._test_correct_calculate_for_month("2003", "8", "600")
        self._test_correct_calculate_for_month("2003", "10", "400")

    def test_correct_calculate_for_missing_month(self) -> None:
        answer: str = "Empty"
        url: str = '/'.join(["/calculate", "1900/0"])
        response = self.app.get(url)
        result: str = response.data.decode()
        self.assertEqual(result, answer)

    def _test_correct_calculate_for_year(self, test_year: str, answer: str) -> None:
        url: str = '/'.join(["/calculate", test_year])
        response = self.app.get(url)
        result: str = response.data.decode()
        self.assertTrue(answer in result)

    def _test_correct_calculate_for_month(self, test_year: str, test_month: str, answer: str) -> None:
        url: str = '/'.join(["/calculate", test_year, test_month])
        response = self.app.get(url)
        result: str = response.data.decode()
        self.assertTrue(answer in result)


if __name__ == '__main__':
    unittest.main()
