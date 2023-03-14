import unittest
from datetime import datetime
from freezegun import freeze_time
from module_2.task_4 import app


class MyTestCase(unittest.TestCase):
    _WEEK_PHRASE: tuple = (
        "Хорошего понедельника",
        "Хорошего вторника",
        "Хорошей среды",
        "Хорошего четверга",
        "Хорошей пятницы",
        "Хорошей субботы",
        "Хорошего воскресенья"
    )

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBAG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world'

    @freeze_time("2022-02-22")
    def test_can_get_correct_username_with_weekdate(self) -> None:
        for day in range(1, 8):
            with self.subTest(day=day):
                date = datetime(year=1, month=1, day=day)
                freeze = freeze_time(date)
                freeze.start()
                self._test_can_get_correct_username_with_weekdate("Хорошей среды", day)
                self._test_can_get_correct_username_with_weekdate("Хорошего среды", day)
                self._test_can_get_correct_username_with_weekdate("среда", day)
                freeze.stop()

    def _test_can_get_correct_username_with_weekdate(self, name: str, day: int) -> None:
        url: str = '/'.join([self.base_url, name])
        response = self.app.get(url)
        response_test = response.data.decode()
        correct_answer_str = MyTestCase._WEEK_PHRASE[day - 1]
        self.assertTrue(response_test.count(correct_answer_str) >= 1)


if __name__ == '__main__':
    unittest.main()
