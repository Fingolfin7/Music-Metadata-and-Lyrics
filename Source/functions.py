# remove non ascii characters from a string to avoid a bunch of search and saving errors
def remove_non_ascii(in_string=""):
    while in_string.find("’") != -1:
        in_string = in_string.replace("’", "\'")
    try:
        in_string = in_string.encode("ascii", errors="ignore").decode()
    except UnicodeEncodeError:
        try:
            in_string = in_string.encode("latin-1", errors="ignore").decode()
        except UnicodeEncodeError:
            in_string = in_string.encode("utf-8", errors="ignore").decode()

    return in_string


def remove_special_characters(in_string=""):
    special_chars = "-,:;_()!@#$%^&*=+|[]<>.~`?•/"

    for char in special_chars:
        if in_string.find(char) != -1:
            in_string = in_string.replace(char, "")

    return remove_non_ascii(in_string)