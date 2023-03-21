import os
from flask import Flask


app = Flask(__name__)


@app.route("/uptime", methods=["GET"])
def uptime():
    uptime: str = os.popen('uptime -p').read()[:-1]
    return f"Current uptime is {uptime}"


if __name__ == '__main__':
    app.run(debug=True)
