import datetime
from flask import Flask


app = Flask(__name__)


@app.route('/get_time/now')
def get_current_time():
    current_time = datetime.datetime.now()
    return f"Точное время: {current_time}"


if __name__ == "__main__":
    app.run()
