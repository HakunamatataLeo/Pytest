#import doctest

def add(a,b):
    """
    >>> add(1,2)
    3
    
    >>> add(3,4)
    7

    >>> add(5,6)
    8

    """
    return a + b


if __name__ == "__main__":
    import doctest
    doctest.testmod()

