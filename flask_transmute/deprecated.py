from web_transmute.decorators import PUT, POST, DELETE


def updates(f):
    """
    this labels a function as one that updates data.
    """
    print("updates is deprecated. please use flask_transmute.POST instead.")
    return POST(f)


def creates(f):
    """
    this labels a function as one that creates data.
    """
    print("updates is deprecated. please use flask_transmute.PUT instead.")
    return PUT(f)


def deletes(f):
    """
    this labels a function as one that deletes data.
    """
    print("updates is deprecated. please use flask_transmute.DELETE instead.")
    return DELETE(f)
