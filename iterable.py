
def iterable (x) -> bool:
    '''Return whether a given value is iterable
    through the iter(...) function'''
    try:
        iter(x)
        return True
    except TypeError:
        return False
