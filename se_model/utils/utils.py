from colorama import init, Fore
from markdown import Markdown
from io import StringIO


def info(string: str):
    """
    Prints a information message to the terminal.
    :param {str} string - The message to print.
    """
    init()
    pre = Fore.GREEN + '[INFO] ' + Fore.RESET
    print(pre + string.replace('\n', '\n' + pre))


def warn(string: str):
    """
    Prints a warning message to the terminal.
    :param {str} string - The message to print.
    """
    init()
    pre = Fore.YELLOW + '[WARN] ' + Fore.RESET
    print(pre + string.replace('\n', '\n' + pre))


def debug(string: str):
    """
    Prints a debug message to the terminal.
    :param {str} string - The message to print.
    """
    init()
    pre = Fore.BLUE + '[DEBUG] ' + Fore.RESET
    print(pre + string.replace('\n', '\n' + pre))


def error(string: str):
    """
    Prints an error message to the terminal.
    :param {str} string - The message to print.
    """
    init()
    pre = Fore.RED + '[ERR] ' + Fore.RESET
    print(pre + string.replace('\n', '\n' + pre))


# from https://stackoverflow.com/a/54923798/2713263
def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


def unmark(text):
    # patching Markdown
    Markdown.output_formats["plain"] = unmark_element
    __md = Markdown(output_format="plain")
    __md.stripTopLevelTags = False
    return __md.convert(text)
