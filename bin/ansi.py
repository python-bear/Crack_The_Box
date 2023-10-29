import colorama as cl
from colorama import Fore as fg, Back as bg, Style as st

import re


cl.init(autoreset=True)


def clear_screen():
    print("\033[1J\033[1;1H", end="")


def hide_cursor():
    print("\033[?25l", end="")


def show_cursor():
    print("\033[?25h", end="")


def fg_rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"


def bg_rgb(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"


def color(char: str):
    if char == "1":
        return f"\033[38;2;51;95;245m{st.BRIGHT}\\"
    elif char == "2":
        return f"\033[38;2;35;65;168m{st.BRIGHT}/"
    elif char == "3":
        return f"\033[38;2;245;64;15m{st.BRIGHT}\\"
    elif char == "4":
        return f"\033[38;2;168;44;10m{st.BRIGHT}/"
    elif char == "5":
        return f"\033[38;2;157;244;57m{st.BRIGHT}\\"
    elif char == "6":
        return f"\033[38;2;107;167;39m{st.BRIGHT}/"
    else:
        return f"{st.RESET_ALL}{char}"


def word_wrap(text, line_length):
    if text.isspace():
        return [text]

    text = str(text).replace('\n', '').replace('\r', '')

    lines = []
    current_line = ''

    for index, char in enumerate(text):
        if len(current_line) >= line_length:
            if current_line[-1] not in (' ', '?', '!', ',', '.', '(', ')', '"', "'", '-', '\t'):
                last_space_index = current_line.rfind(' ')
                if last_space_index != -1:
                    next_word = current_line[last_space_index + 1:]
                    current_line = current_line[:last_space_index].strip()
                    lines.append(current_line)
                    current_line = next_word + char
                else:
                    lines.append(current_line)
                    current_line = char

            else:
                lines.append(current_line)
                current_line = char

        else:
            current_line += char

    if current_line.strip() != '':
        lines.append(current_line)

    for line_index in range(len(lines)):
        lines[line_index] = lines[line_index].strip()

    return lines
