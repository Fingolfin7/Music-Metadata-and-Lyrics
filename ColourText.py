import sys
import os
format_codes = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",

    "bright black": "\u001b[30;1m",
    "bright red": "\u001b[31;1m",
    "bright green": "\u001b[32;1m",
    "bright yellow": "\u001b[33;1m",
    "bright blue": "\u001b[34;1m",
    "bright magenta": "\u001b[35;1m",
    "bright cyan": "\u001b[36;1m",
    "bright white": "\u001b[37;1m",

    "background Black": "\u001b[40m",
    "background Red":   "\u001b[41m",
    "background Green": "\u001b[42m",
    "background Yellow":   "\u001b[43m",
    "background Blue":  "\u001b[44m",
    "background Magenta":   "\u001b[45m",
    "background Cyan":  "\u001b[46m",
    "background White": "\u001b[47m",

    "bright background Black": "\u001b[40;1m",
    "bright background Red":   "\u001b[41;1m",
    "bright background Green": "\u001b[42;1m",
    "bright background Yellow":   "\u001b[43;1m",
    "bright background Blue":  "\u001b[44;1m",
    "bright background Magenta":   "\u001b[45;1m",
    "bright background Cyan":  "\u001b[46;1m",
    "bright background White": "\u001b[47;1m",

    "bold":   "\u001b[1m",
    "italic":   "\u001b[3m",
    "underline":  "\u001b[4m",
    "reversed": "\u001b[7m",
    "crossed": "\u001b[9m",

    "reset": "\u001b[0m"
}


def format_text(line="", colour_code=0):
    for code in format_codes:
        line = line.replace("[" + code + "]", format_codes.get(code))
        line = line.replace("[_text256]", u"\u001b[38;5;" + str(colour_code) + "m")
        if line.__contains__("[_text256_"):
            startIndex = line.index("[_text256_") + len("[_text256_")
            endIndex = line.index("_]")
            colour_code = int(str(line[startIndex:endIndex]))
            subStr = "[_text256_" + str(colour_code) + "_]"
            line = line.replace(subStr, u"\u001b[38;5;" + str(colour_code) + "m")
        line = line.replace("[_background256]", u"\u001b[48;5;" + str(colour_code) + "m")
        if line.__contains__("[__background256_"):
            startIndex = line.index("[__background256_") + len("[__background256_")
            endIndex = line.index("_]")
            colour_code = int(str(line[startIndex:endIndex]))
            subStr = "[__background256_" + str(colour_code) + "_]"
            line = line.replace(subStr, u"\u001b[48;5;" + str(colour_code) + "m")
    return line


def show_256TextColour():
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
        print(u"\u001b[0m")


def show_256BackgroundColour():
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            sys.stdout.write(u"\u001b[48;5;" + code + "m " + code.ljust(4))
        print(u"\u001b[0m")


#  clear = lambda: os.system("cls")
