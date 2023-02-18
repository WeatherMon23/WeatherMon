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
    lst = [word[0].upper() + word[1:] for word in input_str = input_str.split()]
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


def urlDecode(input_str):
    """
    URL decodes a given string

    Parameters
    ----------
    input_str : str
        The string to be decoded

    Returns
    -------
    : str
        The URL decoded string

    """
    input_str = input_str.replace("%20", " ")
    input_str = input_str.replace("+", " ")
    input_str = input_str.replace("%21", "!")
    input_str = input_str.replace("%22", "\"")
    input_str = input_str.replace("%23", "#")
    input_str = input_str.replace("%24", "$")
    input_str = input_str.replace("%25", "%")
    input_str = input_str.replace("%26", "&")
    input_str = input_str.replace("%27", "\'")
    input_str = input_str.replace("%28", "(")
    input_str = input_str.replace("%29", ")")
    input_str = input_str.replace("%30", "*")
    input_str = input_str.replace("%31", "+")
    input_str = input_str.replace("%2C", ",")
    input_str = input_str.replace("%2E", ".")
    input_str = input_str.replace("%2F", "/")
    input_str = input_str.replace("%2C", ",")
    input_str = input_str.replace("%3A", ":")
    input_str = input_str.replace("%3A", "")
    input_str = input_str.replace("%3C", "<")
    input_str = input_str.replace("%3D", "=")
    input_str = input_str.replace("%3E", ">")
    input_str = input_str.replace("%3F", "?")
    input_str = input_str.replace("%40", "@")
    input_str = input_str.replace("%5B", "[")
    input_str = input_str.replace("%5C", "\\")
    input_str = input_str.replace("%5D", "]")
    input_str = input_str.replace("%5E", "^")
    input_str = input_str.replace("%5F", "-")
    input_str = input_str.replace("%60", "`")
    return input_str


def extract_string(s, start):
    """
    Extracts the substring between the last occurrence of start and the first subsequent whitespace character

    Parameters
    ----------
    s : str
        The string which will be searched
    start : str
        Starting location

    Returns
    -------
        The matching string, else None is returned

    """
    index = s.rfind(start)
    if index == -1:
        return None
    index += len(start)
    end_index = len(s)
    for i in range(index, len(s)):
        if s[i].isspace():
            end_index = i
            break
    return s[index:end_index]
