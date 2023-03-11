import datetime
from flask import Flask


app = Flask(__name__)


@app.route('/get_time/future')
def get_current_time_after_hour():
    current_time = datetime.datetime.now()
    current_time_after_hour = current_time + datetime.timedelta(hours=1)
    return f"Точное время: {current_time_after_hour}"


if __name__ == "__main__":
    app.run()
