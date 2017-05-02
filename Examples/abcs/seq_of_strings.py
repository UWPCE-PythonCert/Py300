from collections import abc

def do_something(filenames):
    """
    process a number of files.

    :param filenames: sequence of filenames to process
    """
    for name in filenames:
        print("processing:", name)


def do_something2(filenames):
    """
    process a number of files.

    :param filenames: sequence of filenames to process
    """
    if not isinstance(filenames, abc.Iterable):
        # put it in a tuple so the rest of the code is the same.
        filenames = [filenames]
    for name in filenames:
        print("processing:", name)

def do_something3(filenames):
    """
    process a number of files.

    :param filenames: sequence of filenames to process
    """
    if isinstance(filenames, str):
        # put it in a tuple so the rest of the code is the same.
        filenames = (filenames,)
    for name in filenames:
        print("processing:", name)
