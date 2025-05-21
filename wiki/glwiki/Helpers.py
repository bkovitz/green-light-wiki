# File for various helper functions for refactoring from Py2 to Py3
def cmp(a, b):
    return (a > b) - (a < b)


def apply(func, args, kwargs=None):
    return func(*args) if kwargs is None else func(*args, **kwargs)
