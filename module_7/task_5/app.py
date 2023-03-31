import logging
import logging.config
from module_7.task_5 import utils
from module_7.task_5.dict_config import DICT_CONFIG


def _setup_logger(name: str = __name__) -> logging.Logger:
    logging.config.dictConfig(DICT_CONFIG)
    logger = logging.getLogger(name)
    return logger


logger = _setup_logger("app")


def _show_list_of_commands() -> None:
    logger.info("Start show_list_of_commands()")
    print("Доступные команды:\n"
          "\"+\" - сложение\n"
          "\"-\" - вычитание\n"
          "\"*\" - умножение\n"
          "\"/\" - деление\n"
          "\"^\" - возведение в степень\n")


def _get_command_from_user() -> str:
    logger.info("Start get_command_from_user()")
    command: str = input("Введите выражение с пробелами: ")
    logger.debug(f"Input command: {command}")
    return command


def _process_command(command: str) -> tuple[float, float, str] | None:
    logger.info("Start process_command()")
    command_split: [str] = command.split()
    if len(command_split) != 3:
        logger.warning(f"Incorrect command: {command}")
        return None

    number_1 = float(command_split[0])
    number_2 = float(command_split[2])
    operation = command_split[1]
    logger.debug(f"Processed command: {number_1}, {number_2}, {operation}.")
    return number_1, number_2, operation


def _get_result(command: tuple[float, float, str] | None) -> str:
    logger.info("Start get_result()")
    if command is None:
        logger.debug("Reaction on incorrect command.")
        return "Вы ввели не корректную строку, повторите попытку."

    number_1, number_2, operation = command
    logger.debug(f"number_1={number_1}, number_2={number_2}, operation={operation}")
    result: float = utils.calculate(number_1, number_2, operation)
    logger.debug(f"Result: {result}")
    return str(result)


def _give_result_to_user(result: str) -> None:
    logger.info("Start give_result_to_user()")
    print(result)


if __name__ == '__main__':
    _show_list_of_commands()
    while True:
        logger.info("Start iteration")
        command: str = _get_command_from_user()
        processed_command = _process_command(command)
        result: str = _get_result(processed_command)
        _give_result_to_user(result)
        logger.info("End iteration")
