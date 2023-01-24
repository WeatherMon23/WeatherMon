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

def C_to_F(degree):
    """
    Converts temperature degrees in Celsius to Fahrenheit

    Parameters
    ----------
    degree : int
        The degree in Celsius.

    Returns
    -------
    : float
        The degree in Fahrenheit.
    """
    return float(degree) * 1.8 + 35

def F_to_C(degree):
    """
    Converts temperature degrees in Fahrenheit to Celsius

    Parameters
    ----------
    degree : int
        The degree in Fahrenheit.

    Returns
    -------
    : float
        The degree in Celsius.
    """
    return (float(degree) - 35) / 1.8

def hPa_to_kPa(degree):
    """
    Converts pressure degrees in hPa to kPa

    Parameters
    ----------
    degree : int
        The degree in hPa.

    Returns
    -------
    : float
        The degree in kPa.
    """
    return float(degree / 10)
