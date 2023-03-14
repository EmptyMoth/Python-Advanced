from flask import Flask

app = Flask(__name__)

_storage: dict = {}


def get_storage_value(date: str) -> int:
    year, month, day = _get_date(date)
    return _storage.get(year, {}).get(month, {}).get(day)


@app.route("/add/<date>/<int:value>")
def add_value(date: str, value: int) -> str:
    year, month, day = _get_date(date)
    _storage.setdefault(year, {}) \
        .setdefault(month, {}) \
        .setdefault(day, 0)
    _storage[year][month][day] += value
    return "Successfully!"


@app.route("/calculate/<int:year>")
def calculate_for_year(year: int) -> str:
    if not year in _storage:
        return "Empty"

    days_by_months: dict = _storage[year]
    all_values: [[int]] = [values_by_days.values() for values_by_days in days_by_months.values()]
    result: int = 0
    for values in all_values:
        result += sum(values)
    return str(result)


@app.route("/calculate/<int:year>/<int:month>")
def calculate_for_month(year: int, month: int) -> str:
    days_by_months: dict = _storage.get(year, {})
    values_by_days: dict = days_by_months.get(month, {})
    if values_by_days == {}:
        return "Empty"

    result: int = sum(values_by_days.values())
    return str(result)


def _get_date(date: str) -> (int, int, int):
    return int(date[:4]), int(date[4:6]), int(date[6:])


if __name__ == "__main__":
    app.run(debug=True)
