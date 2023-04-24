import sqlite3


def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str,
) -> bool:
    sql: str = """
    SELECT COUNT(timestamp) >= 3
    FROM table_truck_with_vaccine
    WHERE truck_number = ? AND temperature_in_celsius NOT BETWEEN 16 AND 20
    """

    cursor.execute(sql, (truck_number, ))
    has_spoiled, *_ = cursor.fetchone()
    return bool(has_spoiled)


if __name__ == '__main__':
    with sqlite3.connect("database/hw.db") as connect:
        truck_number: str = input("Введите номер машины\n>")
        cursor: sqlite3.Cursor = connect.cursor()
        has_spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
