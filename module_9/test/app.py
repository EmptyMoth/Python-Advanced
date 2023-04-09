import os
from flask import Flask


HOST = '0.0.0.0'
PORT = 5000
SERVICE_NAME = os.environ.get('SERVICE_NAME', 'application')

app = Flask(__name__)


@app.route("/")
def hello_world() -> str:
    return f"Hello World from {SERVICE_NAME}"


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
