import warnings
from typing import Callable


def deprecated(message: str) -> Callable:
    def deprecated_decorator(func: Callable) -> Callable:
        def deprecated_func(*args, **kwargs) -> Callable:
            warnings.warn(
                f"{func.__name__} is a deprecated function. {message}",
                category=DeprecationWarning,
                stacklevel=2,
            )
            warnings.simplefilter("default", DeprecationWarning)
            return func(*args, **kwargs)

        return deprecated_func

    return deprecated_decorator
