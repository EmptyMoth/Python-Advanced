from flask import Flask


app = Flask(__name__)

# Можно хранить для каждого дня отдельно, но в данной задаче это менее эффективно
_data: dict = {}


@app.route("/add/<date>/<int:value>")
def add_value(date: str, value: int) -> str:
    year: int = int(date[:4])
    month: int = int(date[4:6])
    day: int = int(date[6:])
    _data.setdefault(year, {}).setdefault(month, 0)
    _data[year][month] += value
    return "Successfully!"


@app.route("/calculate/<int:year>")
def calculate_for_year(year: int) -> str:
    sum_by_months: dict = _data.get(year, {})
    result: int = sum(sum_by_months.values())
    return str(result)


@app.route("/calculate/<int:year>/<int:month>")
def calculate_for_month(year: int, month: int) -> str:
    sum_by_months: dict = _data.get(year, {})
    result: int = sum_by_months.get(month, 0)
    return str(result)


if __name__ == "__main__":
    app.run(debug=True)
