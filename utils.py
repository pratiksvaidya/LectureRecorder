from __future__ import print_function

from colorama import Fore, Style

def print_info(text, ret=False):
    output = Fore.CYAN + text
    output += Style.RESET_ALL
    if ret:
        return output
    else:
        print(output)

def print_success(text, ret=False):
    output = Fore.GREEN + text
    output += Style.RESET_ALL
    if ret:
        return output
    else:
        print(output)

def print_error(text, ret=False):
    output = Fore.RED + text
    output += Style.RESET_ALL
    if ret:
        return output
    else:
        print(output)

def print_warning(text, ret=False):
    output = Fore.YELLOW + text
    output += Style.RESET_ALL
    if ret:
        return output
    else:
        print(output)
