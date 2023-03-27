import re


WORDS: set[str] = set()


def is_strong_password(password: str) -> bool:
    for word in WORDS:
        if len(word) > len(password):
            continue

        if word in password:
            return False
    return True


def _filter_out_words(words: [str]) -> set[str]:
    result: set[str] = set()
    min_size_word: int = 5+1
    for word in words:
        if len(word) >= min_size_word:
            result.add(word[:-1])

    return result


if __name__ == '__main__':
    with open("/usr/share/dict/words", 'r') as words:
        WORDS = _filter_out_words(words.readlines())

    print(is_strong_password("asf2basementafawgtags"))
