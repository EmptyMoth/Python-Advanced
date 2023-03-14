import unittest
from task_4 import Person


class TestPerson(unittest.TestCase):
    def setUp(self) -> None:
        self.person = Person("Daler", 2003, "House 3")

    def test_get_age(self):
        age: int = self.person.get_age()
        self.assertTrue(age >= 0)

    def test_get_name(self):
        self.assertEqual(self.person.get_name(), self.person.name)

    def test_get_address(self):
        self.assertEqual(self.person.get_address(), self.person.address)

    def test_set_name(self):
        last_name: str = self.person.name
        new_name: str = "Amir"
        self.person.set_name(new_name)
        self.assertTrue(self.person.name != last_name)

    def test_set_address(self):
        last_address: str = self.person.address
        new_address: str = "House 4"
        self.person.set_address(new_address)
        self.assertTrue(self.person.address != last_address)

    def test_is_homeless(self):
        self.person.set_address(None)
        self.assertTrue(self.person.is_homeless())

    def test_not_is_homeless(self):
        self.assertFalse(self.person.is_homeless())


if __name__ == '__main__':
    unittest.main()
