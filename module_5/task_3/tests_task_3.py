import unittest
from module_5.task_3.task_3 import BlockErrors


class MyTestCase(unittest.TestCase):
    def test_error_is_ignored(self) -> None:
        err_types = {ZeroDivisionError, TypeError}
        with BlockErrors(err_types):
            a = 1 / 0

        self.assertTrue(True)

    def test_child_errors_are_ignored(self) -> None:
        err_types = {BaseException}
        with BlockErrors(err_types):
            raise SystemExit

        self.assertTrue(True)

    def test_non_child_errors_are_not_ignored(self) -> None:
        with self.assertRaises(SystemExit):
            err_types = {Exception}
            with BlockErrors(err_types):
                raise SystemExit

    def test_error_is_thrown_higher_not_is_ignored(self) -> None:
        with self.assertRaises(TypeError):
            outer_err_types = {ZeroDivisionError}
            with BlockErrors(outer_err_types):
                with BlockErrors(outer_err_types):
                    a = 1 / '0'

    def test_error_is_thrown_higher_is_ignored(self) -> None:
        outer_err_types = {TypeError}
        with BlockErrors(outer_err_types):
            inner_err_types = {ZeroDivisionError}
            with BlockErrors(inner_err_types):
                a = 1 / '0'

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
