import sqlite3
import csv


def delete_wrong_fees(cursor: sqlite3.Cursor, wrong_fees_file: str) -> None:
    with open(wrong_fees_file) as file:
        sql: str = """
        DELETE FROM table_fees
        WHERE truck_number = ? AND timestamp = ?
        """

        data: [[str]] = [line for line in csv.reader(file)]
        cursor.executemany(sql, data)


if __name__ == "__main__":
    with sqlite3.connect("../database/hw.db") as conn:
        cursor = conn.cursor()

        delete_wrong_fees(cursor, "wrong_fees.csv")
