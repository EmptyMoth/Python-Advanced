import unittest
from module_2.task_3 import decrypt


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.one_dot: dict = {
            "абра-кадабра.": "абра-кадабра",
            ".": "",
        }

        cls.two_dot: dict = {
            "абраа..-кадабра": "абра-кадабра",
            "абра--..кадабра": "абра-кадабра",
        }

        cls.many_dot: dict = {
            "абраа..-.кадабра": "абра-кадабра",
            "абрау...-кадабра": "абра-кадабра",
            "абра........": "",
            "абр......a.": "a",
            "1..2.3": "23",
            "1.......................": "",
        }

    def test_correct_decrypt_for_one_dot(self) -> None:
        for test_data, answer in self.one_dot.items():
            with self.subTest(test_data=test_data, answer=answer):
                self._test_correct_decrypt(test_data, answer)

    def test_correct_decrypt_for_two_dot(self) -> None:
        for test_data, answer in self.two_dot.items():
            with self.subTest(test_data=test_data, answer=answer):
                self._test_correct_decrypt(test_data, answer)

    def test_correct_decrypt_for_many_dot(self) -> None:
        for test_data, answer in self.many_dot.items():
            with self.subTest(test_data=test_data, answer=answer):
                self._test_correct_decrypt(test_data, answer)

    def _test_correct_decrypt(self, test_data: str, answer: str) -> None:
        result: str = decrypt(test_data)
        self.assertEqual(result, answer)


if __name__ == '__main__':
    unittest.main()
