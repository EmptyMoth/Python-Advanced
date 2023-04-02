import os
import json
import subprocess
import shlex
from _datetime import datetime
from itertools import groupby


ROOT_DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))
PATH_TO_LOG: str = os.path.join(ROOT_DIRECTORY, "skillbox_json_messages.log")

LEVELS: [str] = ["DEBUG", "INFO", "WARNING", "ERROR", "FATAL", "CRITICAL"]


def get_filtered_logs(log: str) -> dict:
    logs: [dict] = []
    with open(log, 'r') as file:
        for log in file:
            logs.append(json.loads(log))

    levels = lambda x: x["level"]
    sorted_logs = sorted(logs, key=levels)
    filter_logs: dict = {}
    for level, logs in groupby(sorted_logs, key=levels):
        filter_logs[level] = [log for log in logs]
    return filter_logs


def counts_logs_for_all_levels(logs: dict) -> [tuple[str, int]]:
    result: list = []
    for level in LEVELS:
        log: list[dict] = logs.get(level, [])
        result.append((level, len(log)))

    return result


def get_hour_with_largest_number_of_logs(all_logs: dict) -> int:
    most_common_hour: int = 0
    max_count: int = 0
    for level, logs in all_logs.items():
        time_list: [datetime] = [datetime.strptime(log.get("time", "0"), "%H:%M:%S") for log in logs]
        time_list.sort()
        for time, group in groupby(time_list):
            count: int = len(list(group))
            if count > max_count:
                max_count = count
                most_common_hour = time.hour

    return most_common_hour


def count_logs_with_level_at_certain_time(logs: [dict], str_time_begin: str, str_time_end: str) -> int:
    number_of_logs_at_certain_time: int = 0
    time_begin: datetime = datetime.strptime(str_time_begin, "%H:%M:%S")
    time_end: datetime = datetime.strptime(str_time_end, "%H:%M:%S")
    for log in logs:
        str_time: str = log.get("time", "")
        time: datetime = datetime.strptime(str_time, "%H:%M:%S")
        if time_begin <= time <= time_end:
            number_of_logs_at_certain_time += 1

    return number_of_logs_at_certain_time


def count_logs_with_message(file: str, message: str) -> int:
    command: str = f"grep -c '{message}' {file}"
    args: [str] = shlex.split(command)
    print(file, command, args)
    result = subprocess.run(args=args, capture_output=True, encoding="UTF-8")
    return int(result.stdout)


def get_most_common_word_for_level_in_logs(logs: [dict]) -> str:
    most_common_word: str = ""
    max_count: int = 0
    words: [str] = [log.get("message", '') for log in logs]
    words.sort()
    for word, group in groupby(words):
        count: int = len(list(group))
        if count > max_count:
            max_count = count
            most_common_word = word

    return most_common_word


if __name__ == '__main__':
    logs: dict = get_filtered_logs(PATH_TO_LOG)
    print(counts_logs_for_all_levels(logs))
    print(get_hour_with_largest_number_of_logs(logs))
    print(count_logs_with_level_at_certain_time(logs[LEVELS[-1]], "05:00:00", "05:20:00"))
    print(count_logs_with_message(PATH_TO_LOG, "dog"))
    print(get_most_common_word_for_level_in_logs(logs.get(LEVELS[2], [])))
