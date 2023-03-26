import subprocess
import shlex
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange

app = Flask(__name__)


class RemoteCode(FlaskForm):
    code = StringField(validators=[InputRequired()])
    timeout = IntegerField(validators=[InputRequired(), NumberRange(min=0, max=30)])


@app.route("/python", methods=["POST"])
def python_code():
    form = RemoteCode()

    if form.validate_on_submit():
        return _execute_code(form.code.data, form.timeout.data)
    return f"Invalid input, {form.errors}", 400


def _execute_code(code: str, timeout: int) -> str:
    code = code.replace('"', '\\"')
    command: str = f'prlimit --nproc=1:1 python3 -c "{code}"'
    args: [str] = shlex.split(command)
    process = subprocess.Popen(args=args, encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        outs, errs = process.communicate(timeout=timeout)
        return outs
    except subprocess.TimeoutExpired:
        process.kill()
        return "Программа не уложилась в поставленное время"


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
