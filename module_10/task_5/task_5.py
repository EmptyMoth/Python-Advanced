def find_insert_position(sorted_list: list[int], x: int) -> int:
    if len(sorted_list) == 0 or sorted_list[0] >= x:
        return 0
    elif sorted_list[-1] <= x:
        return len(sorted_list)
    return _binary_search(sorted_list, x)


def _binary_search(sorted_list: list[int], x: int) -> int:
    left_border: int = 0
    right_border: int = len(sorted_list) - 1
    while left_border < right_border:
        point: int = left_border + (right_border - left_border) // 2
        element = sorted_list[point]
        if x < element:
            right_border = point - 1
        elif x > element:
            left_border = point + 1
        else:
            return point

    return left_border


if __name__ == '__main__':
    A = [1, 2, 3, 3, 3, 5]
    x = 4
    print(find_insert_position(A, x))
