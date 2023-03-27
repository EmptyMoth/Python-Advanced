import re


WORDS: str = ''
PHONE: dict[str, str] = {
    '2': '[abc]',
    '3': '[def]',
    '4': '[ghi]',
    '5': '[jkl]',
    '6': '[mno]',
    '7': '[pqrs]',
    '8': '[tuv]',
    '9': '[wxyz]'
}


def my_t9(code: str) -> [str]:
    for number, values in PHONE.items():
        code = code.replace(number, values)

    result: [str] = re.findall(rf"(?i){code}", WORDS)
    return result


if __name__ == '__main__':
    with open("/usr/share/dict/words", 'r') as words:
        WORDS = words.read()

    print(my_t9("22736368"))
