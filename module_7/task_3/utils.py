import math
import logging


logger = logging.getLogger(name="utils")


def calculate(a: float, b: float, operation: str) -> float:
    logger.info("Start calculate()")
    match operation:
        case "+":
            return _addition(a, b)
        case "-":
            return _subtraction(a, b)
        case "*":
            return _multiplication(a, b)
        case "/":
            return _division(a, b)
        case "^":
            return _pow(a, b)


def _addition(a: float, b: float) -> float:
    logger.info("Start addition()")
    result: float = a + b
    logger.debug(f"Result: {a}+{b}={result}")
    return result


def _subtraction(a: float, b: float) -> float:
    logger.info("Start subtraction()")
    result: float = a - b
    logger.debug(f"Result: {a}-{b}={result}")
    return result


def _multiplication(a: float, b: float) -> float:
    logger.info("Start multiplication()")
    result: float = a * b
    logger.debug(f"Result: {a}*{b}={result}")
    return result


def _division(a: float, b: float) -> float:
    logger.info("Start division()")
    result: float = a / b
    logger.debug(f"Result: {a}/{b}={result}")
    return result


def _pow(a: float, b: float) -> float:
    logger.info("Start pow()")
    result: float = math.pow(a, b)
    logger.debug(f"Result: {a}^{b}={result}")
    return result
