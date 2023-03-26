import unittest
from module_5.task_4.task_4 import Redirect


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stdout_path: str = r'.\stdout.txt'
        cls.stderr_path: str = r'.\stderr.txt'
        cls.stdout_message: str = 'Hello stdout.txt'
        cls.stderr_message: str = 'Hello stderr.txt'

    def setUp(self) -> None:
        self.stdout_file = open(self.stdout_path, 'w')
        self.stderr_file = open(self.stderr_path, 'w')

    def test_full_context_manager(self):
        with Redirect(stdout=self.stdout_file, stderr=self.stderr_file):
            print(self.stdout_message)
            raise Exception(self.stderr_message)

        with open(self.stdout_path, 'r') as stdout:
            self.assertIn(self.stdout_message, stdout.read())
        with open(self.stderr_path, 'r') as stderr:
            self.assertIn(self.stderr_message, stderr.read())

    def test_only_stdout(self):
        with Redirect(stdout=self.stdout_file):
            print(self.stdout_message)

        with open(self.stdout_path, 'r') as stdout:
            self.assertIn(self.stdout_message, stdout.read())

    def test_only_stderr(self):
        with Redirect(stderr=self.stderr_file):
            raise Exception(self.stderr_message)

        with open(self.stderr_path, 'r') as stderr:
            self.assertIn(self.stderr_message, stderr.read())

    def test_empty_context_manager(self):
        with Redirect():
            pass
        self.assertTrue(True)


if __name__ == '__main__':
    with open(r'./test_results.txt', 'a') as test_file_stream:
        runner = unittest.TextTestRunner(stream=test_file_stream)
        unittest.main(testRunner=runner)
