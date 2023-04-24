import sqlite3


SALARY_IVAN_SOVIN: int = 100_000


def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor, name: str,) -> None:
    promote_employee(cursor, name)
    dismiss_employee_if_his_salary_is_higher(cursor, name)


def promote_employee(
        cursor: sqlite3.Cursor, name: str) -> None:
    cursor.execute("""
    UPDATE table_effective_manager 
    SET salary = 1.1 * salary
    WHERE name = ? AND name != 'Иван Совин'
    """, (name, ))


def dismiss_employee_if_his_salary_is_higher(
        cursor: sqlite3.Cursor, name: str) -> None:
    cursor.execute("""
    DELETE FROM table_effective_manager
    WHERE name = ? AND salary > ?
    """, (name, SALARY_IVAN_SOVIN))


if __name__ == "__main__":
    name = input("Пожалуйста введите имя сотрудника\n> ")
    with sqlite3.connect("./database/hw.db") as connection:
        cursor = connection.cursor()
        ivan_sovin_the_most_effective(cursor, name)
