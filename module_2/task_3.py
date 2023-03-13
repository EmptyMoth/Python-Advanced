import sys


_test_data: dict = {
    "абра-кадабра.": "абра-кадабра",
    "абраа..-кадабра": "абра-кадабра",
    "абраа..-.кадабра": "абра-кадабра",
    "абра--..кадабра": "абра-кадабра",
    "абрау...-кадабра": "абра-кадабра",
    "абра........": "",
    "абр......a.": "a",
    "1..2.3": "23",
    ".": "",
    "1.......................": "",
}


def decrypt(text: str) -> str:
    new_text: str = ""
    text = text.replace("..", "!")
    text = text.replace(".", "")
    for i in range(len(text)):
        if text[i] == '!':
            new_text = new_text[:len(new_text) - 1]
        else:
            new_text = ''.join([new_text, text[i]])

    print(new_text)
    return new_text


def _tests() -> None:
    for string, result in _test_data.items():
        answer: str = decrypt(string)
        if answer != result:
            raise Exception("Ancorrect answer")


if __name__ == "__main__":
    input_text: str = sys.stdin.read()
    #_tests()
    decrypt(input_text)
