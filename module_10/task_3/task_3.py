import sqlite3


def _execute_sql_code(database: sqlite3.Connection, sql: str) -> list:
    cursor = database.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def _count_number_of_records_in_tables(
        database: sqlite3.Connection, tables: [str]) -> dict:
    result: list = []
    for table in tables:
        count_records: list = _execute_sql_code(
            database,
            sql=f"SELECT COUNT(*) FROM {table}")
        result.append((table, count_records))

    return dict(result)


def _count_number_of_crossed_records_in_tables(
        database: sqlite3.Connection, tables: [str]) -> list:
    commands_list: [str] = [f"SELECT {table}.value FROM {table}" for table in tables]
    commands: str = " INTERSECT ".join(commands_list)
    sql: str = f"SELECT COUNT(*) FROM ({commands})"

    result: list = _execute_sql_code(database, sql=sql)
    return result


if __name__ == '__main__':
    with sqlite3.connect("./hw_3_database.db") as database:
        print("1.", _count_number_of_records_in_tables(
            database, tables=["table_1", "table_2", "table_3"]))
        print("2.", _execute_sql_code(
            database, sql="SELECT COUNT(DISTINCT value) FROM  table_1"))
        print("3.", _count_number_of_crossed_records_in_tables(
            database, tables=["table_1", "table_2"]))
        print("4.", _count_number_of_crossed_records_in_tables(
            database, tables=["table_1", "table_2", "table_3"]))
