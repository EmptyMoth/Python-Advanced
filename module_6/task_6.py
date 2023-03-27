from flask import Flask


app = Flask(__name__)


@app.route("/1", methods=["GET"])
def func_1() -> str:
    return "OK"


@app.route("/2", methods=["GET"])
def func_2() -> str:
    return "OK"


@app.route("/3", methods=["GET"])
def func_3() -> str:
    return "OK"


@app.errorhandler(404)
def handler_not_found(ex: 404):
    header: str = "<h4>Данная страница не доступна. Доступны следующие ссылки.</h4><h3>Карта сайта:</h3>"

    links: [str] = _get_rules()
    result: str = '\n'.join(links)
    body = f"{header}<ul>{result}</ul>"

    return body


def _get_rules() -> [str]:
    links: [str] = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and _has_no_empty_params(rule):
            links.append(f"<li><a href=\"{rule}\">{rule}</a></li>")
    return links


def _has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


if __name__ == '__main__':
    app.run(debug=True)