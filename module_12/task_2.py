import subprocess


def process_count(username: str) -> int:
    command: str = f"pgrep -u {username} -l | wc -l"
    result: str = _execute_command(command)
    return int(result)


def total_memory_usage(root_pid: int) -> float:
    command: str = "|".join([f"ps -h --ppid {root_pid} -o pmem", "awk '{ SUM += $1 } END { print SUM }'"])
    result: str = _execute_command(command)
    return float(result)


def _execute_command(command: str) -> str:
    result = subprocess.run(args=command, shell=True, capture_output=True, encoding='utf-8')
    return result.stdout


if __name__ == '__main__':
    print(process_count("root"))
    print(total_memory_usage(1))
