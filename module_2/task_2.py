import sys


_NUMBER_OF_COLUMN_WITH_SIZE: int = 4


def get_mean_size(files: [str]) -> float:
    summary_size: int = 0
    for file in files:
        columns: [str] = file.split()
        summary_size += int(columns[_NUMBER_OF_COLUMN_WITH_SIZE])

    mean_size: float = summary_size
    if len(files) > 0:
        mean_size /= len(files)
    print(mean_size)
    return mean_size


if __name__ == "__main__":
    lines: [str] = sys.stdin.readlines()[1:]
    get_mean_size(lines)
