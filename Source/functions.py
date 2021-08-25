import unidecode
import re

# remove non ascii characters from a string to avoid a bunch of search and saving errors
def remove_non_ascii(in_string=""):
    in_string = in_string.strip("​")
    in_string = re.sub("[•]", "", in_string)
    in_string = unidecode.unidecode(in_string)

    try:
        in_string = in_string.encode("ascii", errors="ignore").decode()
    except UnicodeEncodeError:
        try:
            in_string = in_string.encode("latin-1", errors="ignore").decode()
        except UnicodeEncodeError:
            in_string = in_string.encode("utf-8", errors="ignore").decode()

    return in_string


def remove_special_characters(in_string=""):
    # special_chars = "-,:;_()!@#$%^&*=+|[]<>.~`?•/"

    in_string = re.sub('[^a-zA-Z0-9 \'\n.]', "", in_string)

    return remove_non_ascii(in_string)


def main():
    print(remove_non_ascii(input(">")))
    input()


if __name__ == "__main__":
    main()
