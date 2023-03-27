import getpass
import hashlib
import logging


logger = logging.getLogger("password_checker")


def input_and_check_password() -> bool:
    password: str = getpass.getpass()

    if password == "":
        logger.warning("Вы ввели пустой пароль.")
        return False

    try:
        hasher = hashlib.md5()
        hasher.update(password.encode("latin-1"))
        if hasher.hexdigest() == "c96dd568316deb9d8c7dec73b4c27cbb":
            logger.info("Вы успешно вошли в систему.")
            return True
    except ValueError as exception:
        logger.exception("Вы ввели некорректный символ", exc_info=exception)

    return False


if __name__ == "__main__":
    logging.basicConfig(filename="./stderr.txt",
                        level=logging.INFO,
                        datefmt="%H:%M:%S",
                        format="%(asctime)s: %(message)s")

    logger.debug("Начало")
    logger.info("Вы пытаетесь аутентифицироваться в систему.")
    count_number: int = 3
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        count_number -= 1
        if input_and_check_password():
            exit(0)

    logger.error("Пользователь трижды ввёл неправильный пароль!")
    exit(1)
