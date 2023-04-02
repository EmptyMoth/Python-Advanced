import os
from flask import Flask, render_template


#root_dir: str = os.path.dirname(os.path.abspath(__file__))
#templates_dir: str = os.path.join(root_dir, "templates")
#static_dir: str = os.path.join(root_dir, "static")


app = Flask(__name__)


@app.route("/index")
def hello_world() -> str:
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
