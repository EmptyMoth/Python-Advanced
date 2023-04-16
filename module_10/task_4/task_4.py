import sqlite3


POVERTY_LINE: int = 5000


def _execute_sql_code(database: sqlite3.Connection, sql: str) -> list:
    cursor = database.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


if __name__ == '__main__':
    with sqlite3.connect("hw_4_database.db") as database:
        print("1.", _execute_sql_code(
            database, sql=f"SELECT COUNT(salary) FROM salaries WHERE salary < {POVERTY_LINE}"))
        print("2.", _execute_sql_code(
            database, sql="SELECT AVG(salary) FROM salaries"))
        print("3.", _execute_sql_code(
            database, sql="""
            SELECT AVG(salary) FROM (
                SELECT salary FROM salaries
                ORDER BY salary
                LIMIT 2 OFFSET FLOOR(0.5 * (SELECT COUNT(salary) FROM salaries))
            );
        """))
        print("4.", _execute_sql_code(
            database, sql="""
            SELECT 100 * ROUND(TOP10 / CAST(DOWN90 AS real), 2) FROM (
                (
                    SELECT SUM(salary) as TOP10 FROM (
                    SELECT salary
                    FROM salaries
                    ORDER BY salary DESC
                    LIMIT 0.1 * (SELECT COUNT(salary) FROM salaries)
                ))
                JOIN
                (
                    SELECT SUM(salary) as DOWN90 FROM (
                    SELECT salary
                    FROM salaries
                    ORDER BY salary
                    LIMIT 0.9 * (SELECT COUNT(salary) FROM salaries)
                ))
            )
        """))
