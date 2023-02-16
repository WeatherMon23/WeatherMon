""" UTILS """


def capitalize_first_letter(s):
    """
    Capitilizes the first letter of each word in a given sentence.
    Parameters
    ----------
    s : str
        The sentence we want to capitalize.
    Returns
    -------
    s : str
        The modified sentence.
    """
    lst = [word[0].upper() + word[1:] for word in s.split()]
    s = " ".join(lst)
    return s


def add_left_zero(s):
    """
    Adds '0' to the left of a string.

    Parameters
    ----------
    s : str
        The string we want to modify.

    Returns
    -------
    : str
        The string with a '0' concatentated to its left.
    """
    if len(s) == 1:
        return '0' + s
    else:
        return s
