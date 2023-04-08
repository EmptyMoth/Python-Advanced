from flask import Flask


HOST = '0.0.0.0'
PORT = 5000

app = Flask(__name__)


@app.route("/")
def hello_world() -> str:
    return "<h1>Hello World</h1>"


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
