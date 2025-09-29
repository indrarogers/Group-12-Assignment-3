# Defines functions for utility decorators and helpers, demonstrates multiple decorators used

import time
from functools import wraps
import sys

def simple_logger(message):
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{ts}] {message}", file=sys.stderr)

def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        simple_logger(f"Timing: {func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

def cached_result(func):
    cache = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        # create a simple key ignoring unhashable objects
        try:
            key = (func.__name__, args[1:] if len(args) > 1 else (), frozenset(kwargs.items()))
        except Exception:
            key = (func.__name__,)
        if key in cache:
            simple_logger(f"cached_result: returning cached result for {func.__name__}")
            return cache[key]
        res = func(*args, **kwargs)
        cache[key] = res
        return res
    return wrapper
