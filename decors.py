import warnings
from functools import wraps

def depricated(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"{function.__name__} is depricated, please change.",
            DeprecationWarning,
            stacklevel=2
        )
        return function(*args, **kwargs)
    return wrapper
