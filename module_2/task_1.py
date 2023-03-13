_file_path: str = "./output_file.txt"


def get_summary_rss(file_path: str) -> tuple:
    with open(file_path) as file:
        summary_rss: int = 0
        first_line: [str] = file.readline().split()
        index_rss: int = first_line.index("RSS")
        for line in file:
            columns: [str] = line.split()
            summary_rss += int(columns[index_rss])

        return convert_in_format(summary_rss)


def convert_in_format(bytes: int) -> tuple:
    data: [int] = [bytes, 0, 0, 0, 0]
    for i in range(1, len(data)):
        data[i] = data[i-1] // 1024
        data[i-1] %= 1024

    print(data)
    return tuple(data)


if __name__ == "__main__":
    get_summary_rss(_file_path)
