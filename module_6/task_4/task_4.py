import os
import json
import subprocess
import shlex


ROOT_DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))
PATH_TO_LOG: str = os.path.join(ROOT_DIRECTORY, "skillbox_json_messages.log")


def count_logs_with_message(file: str, message: str) -> int:
    command: str = f"grap -c '{message}' {file}"
    args: [str] = shlex.split(command)
    result = subprocess.run(args=args, capture_output=True, encoding="UTF-8")
    return int(result)


if __name__ == '__main__':
    print(count_logs_with_message(PATH_TO_LOG, "dog"))
    with open("./skillbox_json_messages.log", 'r') as file:
        for line in file:
            j = json.loads(line)
            print(j)