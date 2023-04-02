import os
from flask import Flask, render_template, send_from_directory


root_dir: str = os.path.dirname(os.path.abspath(__file__))

css_directory: str = os.path.join(root_dir, "css")
js_directory: str = os.path.join(root_dir, "java-script")
img_directory: str = os.path.join(root_dir, "img")


app = Flask(__name__)


@app.route("/index")
def hello_world() -> str:
    return render_template("index.html")


@app.route("/css/<path:path>")
def send_css(path: str):
    return send_from_directory(css_directory, path)


@app.route("/js/<path:path>")
def send_js(path: str):
    return send_from_directory(js_directory, path)\


@app.route("/img/<path:path>")
def send_img(path: str):
    return send_from_directory(img_directory, path)


if __name__ == '__main__':
    app.run(debug=True)
