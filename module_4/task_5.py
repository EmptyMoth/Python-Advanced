import shlex
import subprocess
from flask import Flask, request


app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def uptime():
    args: list[str] = request.args.getlist('arg', type=str)
    if args is None:
        return "No args", 400

    command: list[str] = _get_correct_command("ps", "".join(args))
    result: str = _get_result_command(command)
    return f"<pre>{command}\n{result}</pre>"


def _get_correct_command(main_cmd: str, user_cmd: str) -> list[str]:
    clean_user_cmd: str = shlex.quote(user_cmd)
    command_str: str = f"{main_cmd} {clean_user_cmd}"
    command: list[str] = shlex.split(command_str)
    return command


def _get_result_command(command: list[str]) -> str:
    command_result = subprocess.run(command, capture_output=True)
    command_result.check_returncode()
    result = str(command_result.stdout).replace('\\n', "\n")
    return result


if __name__ == '__main__':
    app.run(debug=True)
