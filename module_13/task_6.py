import math
import sqlite3
import datetime

EMPLOYEES_PER_SHIFT_COUNT: int = 10
WORKING_DAYS_COUNT: int = 366
EMPLOYEES_COUNT: int = 366
WORKED_SHIFTS_FOR_ONE_EMPLOYEE_COUNT: int = WORKING_DAYS_COUNT * EMPLOYEES_PER_SHIFT_COUNT // EMPLOYEES_COUNT
FREQUENCY_OF_RECURRING_SHIFTS: float = WORKING_DAYS_COUNT / WORKED_SHIFTS_FOR_ONE_EMPLOYEE_COUNT
UNIQUE_SHIFTS_COUNT: int = EMPLOYEES_COUNT // WORKED_SHIFTS_FOR_ONE_EMPLOYEE_COUNT
DATE_OF_FIRST_WORKING_DAY: datetime.datetime = datetime.datetime(year=2020, month=1, day=1)
SPORTS: [str] = ["футбол", "хоккей", "шахматы", "SUP сёрфинг", "бокс", "Dota2", "шах-бокс"]
ALL_DATES: [datetime.datetime] = [DATE_OF_FIRST_WORKING_DAY + datetime.timedelta(days=i)
                                  for i in range(WORKING_DAYS_COUNT)]


def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    employees_by_weekday: dict[int, list] = _get_employees_by_weekday(cursor)
    shifts: dict[int, [int]] = _get_shifts(employees_by_weekday)
    schedule: [tuple[int, str]] = _get_schedule(shifts)
    _update_work_schedule(cursor, schedule)


def _get_employees_by_weekday(cursor: sqlite3.Cursor) -> dict[int, list]:
    employees_by_weekday: dict[int, list] = {}
    for i in range(len(SPORTS)):
        cursor.execute("""
                SELECT id
                FROM table_friendship_employees
                WHERE preferable_sport = ?
            """, (SPORTS[i],))
        employees_by_weekday[i] = cursor.fetchall()

    return employees_by_weekday


def _get_shifts(employees_by_weekday: dict[int, list]) -> dict[int, [int]]:
    shifts: dict[int, [int]] = {}
    for weekday in [ALL_DATES[i].weekday() for i in range(UNIQUE_SHIFTS_COUNT + 1)]:
        shifts.setdefault(weekday, [])
        employees_for_shifts: list = _get_employees_for_shifts(employees_by_weekday, weekday)
        shifts[weekday].append(employees_for_shifts)

    return shifts


def _get_employees_for_shifts(employees_by_weekday: dict[int, list], weekday: int) -> list:
    employees_for_shifts: list = []
    for i in range(1, 7):
        key = (weekday + i) % 7
        if key == weekday:
            continue

        employees: [tuple] = employees_by_weekday[key]
        if len(employees) <= 0:
            continue
        remaining_places_on_shift_count: int = EMPLOYEES_PER_SHIFT_COUNT - len(employees_for_shifts)
        if remaining_places_on_shift_count <= 0:
            break

        employees_to_be_added_count: int = min(remaining_places_on_shift_count, len(employees))
        for _ in range(employees_to_be_added_count):
            employee_id: int = employees.pop()[0]
            employees_for_shifts.append(employee_id)

    return employees_for_shifts


def _get_schedule(shifts: dict[int, [int]]) -> [tuple[int, str]]:
    schedule: [tuple[int, str]] = []
    for i in range(UNIQUE_SHIFTS_COUNT + 1):
        weekday: int = ALL_DATES[i].weekday()
        shift: [int] = shifts[weekday].pop()
        for j in range(WORKED_SHIFTS_FOR_ONE_EMPLOYEE_COUNT):
            for employee_id in shift:
                number_of_date: int = i + math.floor(j * FREQUENCY_OF_RECURRING_SHIFTS)
                date: str = ALL_DATES[number_of_date].strftime("%Y-%m-%d")
                schedule.append((employee_id, date))

    return schedule


def _update_work_schedule(cursor: sqlite3.Cursor, schedule: [tuple[int, str]]) -> None:
    cursor.executemany("""
        INSERT INTO table_friendship_schedule (employee_id, date)
        VALUES (?, ?)
    """, schedule)


if __name__ == '__main__':
    with sqlite3.connect("./database/hw.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM table_friendship_schedule""")
        update_work_schedule(cursor)
