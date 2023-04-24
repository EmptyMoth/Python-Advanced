import datetime
import sqlite3


def log_bird(cursor: sqlite3.Cursor, bird_name: str, date_time: str) -> None:
    sql: str = """INSERT INTO 'table_birds' (bird_name, date_time) VALUES (?, ?)"""
    cursor.execute(sql, (bird_name, date_time))


def check_if_such_bird_already_seen(cursor: sqlite3.Cursor, bird_name: str) -> bool:
    sql = """
    SELECT EXISTS (
        SELECT *
        FROM 'table_birds'
        WHERE bird_name = ?
    )
    """

    cursor.execute(sql, (bird_name, ))
    such_bird_already_seen, *_ = cursor.fetchone()
    return bool(such_bird_already_seen)


def _create_table(cursor: sqlite3.Cursor) -> None:
    sql: str = """
    CREATE TABLE IF NOT EXISTS table_birds (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,  
    bird_name TEXT NOT NULL,
    date_time TEXT NOT NULL
    )
    """
    cursor.execute(sql)


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name = input("Пожалуйста введите имя птицы\n> ")
    count_str = input("Сколько птиц вы увидели?\n> ")
    count = int(count_str)
    right_now = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("./database/hw.db") as connection:
        cursor = connection.cursor()
        _create_table(cursor)

        log_bird(cursor, name, right_now)
        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")
