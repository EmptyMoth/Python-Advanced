from typing import Iterable


class BlockErrors:
    def __init__(self, errors: Iterable) -> None:
        self.errors: Iterable = errors
        self.there_is_common_exception: bool = Exception in errors

    def __enter__(self) -> None:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool | None:
        for error in self.errors:
            if issubclass(exc_type, error):
                return True