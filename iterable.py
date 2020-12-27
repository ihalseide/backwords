
def iterable (x) -> bool:
    '''Return whether a given value is iterable
    through the iter(...) function'''
    try:
        _ = iter(x)
        return True
    except TypeError:
        return False