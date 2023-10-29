from bin.ansi import *


def coord_in_surf(surface, coordinate):
    row, col = coordinate
    if 0 <= row < len(surface) and 0 <= col < len(surface[0]):
        return True
    else:
        return False


def blit(background, foreground, destination=(0, 0)):
    if not coord_in_surf(background, destination):
        raise CoordNotFound(background, destination)

    final = [row.copy() for row in background]

    dest_row, dest_col = destination

    for row in range(len(foreground)):
        for col, char in enumerate(foreground[row]):
            if 0 <= dest_row + row < len(final) and 0 <= dest_col + col < len(final[row]) and char != " ":
                final[dest_row + row][dest_col + col] = char

    return final


def color_lines(surface, character, ansi_code):
    final = [[char for char in row] for row in surface]

    for row in range(len(surface)):
        for col, char in enumerate(surface[row]):
            if char == character or (character is None and char not in " \r\n\t"):
                final[row][col] = ansi_code + char + st.RESET_ALL

    return final


def minusise(num: int):
    return f"-{num}"


def erase(surface, rect: tuple = None):
    if rect is None:
        return [[' ' for _ in row] for row in surface]

    for i in range(2):
        if not coord_in_surf(surface, (rect[i], rect[i + 2])):
            raise CoordNotFound(surface, (rect[i], rect[i + 2]))

    final = [row.copy() for row in surface]

    dest_row, dest_col = rect[0], rect[1]

    for row in range(rect[0], rect[2] + 1):
        for col in range(rect[1], rect[3] + 1):
            if 0 <= dest_row + row < len(final) and 0 <= dest_col + col < len(final[row]):
                final[dest_row + row][dest_col + col] = " "

    return final


class CoordNotFound(Exception):
    def __init__(self, surface, coordinate):
        super().__init__(f"The coord {coordinate} could not be found in the surface {surface}")


segment_digits = {
    "0": color_lines("┌────┐\n│ ┌┐ │\n│ ││ │\n│ ││ │\n│ └┘ │\n└────┘".split("\n"), None, fg.LIGHTCYAN_EX),
    "1": color_lines("   ┌─┐\n   │ │\n   │ │\n   │ │\n   │ │\n   └─┘".split("\n"), None, fg.LIGHTCYAN_EX),
    "2": color_lines("┌────┐\n└──┐ │\n┌──┘ │\n│ ┌──┘\n│ └──┐\n└────┘".split("\n"), None, fg.LIGHTCYAN_EX),
    "3": color_lines("┌────┐\n└──┐ │\n┌──┘ │\n└──┐ │\n┌──┘ │\n└────┘".split("\n"), None, fg.LIGHTCYAN_EX),
    "4": color_lines("┌─┐┌─┐\n│ ││ │\n│ └┘ │\n└──┐ │\n   │ │\n   └─┘".split("\n"), None, fg.LIGHTCYAN_EX),
    "5": color_lines("┌────┐\n│ ┌──┘\n│ └──┐\n└──┐ │\n┌──┘ │\n└────┘".split("\n"), None, fg.LIGHTCYAN_EX),
    "6": color_lines("┌────┐\n│ ┌──┘\n│ └──┐\n│ ┌┐ │\n│ └┘ │\n└────┘".split("\n"), None, fg.LIGHTCYAN_EX),
    "7": color_lines("┌────┐\n└──┐ │\n   │ │\n   │ │\n   │ │\n   └─┘".split("\n"), None, fg.LIGHTCYAN_EX),
    "8": color_lines("┌────┐\n│ ┌┐ │\n│ └┘ │\n│ ┌┐ │\n│ └┘ │\n└────┘".split("\n"), None, fg.LIGHTCYAN_EX),
    "9": color_lines("┌────┐\n│ ┌┐ │\n│ └┘ │\n└──┐ │\n   │ │\n   └─┘".split("\n"), None, fg.LIGHTCYAN_EX),
    "w": 6,
    "h": 6,
}

safe = "╔══════════════════════════════════════════╗\n" \
       "║ ╭───┬───┬───╮ ╭────────────────────────╮ ║\n" \
       "║ │ 1 │ 2 │ 3 │ │                        │ ║\n" \
       "║ ├───┼───┼───┤ │                        │ ║\n" \
       "║ │ 4 │ 5 │ 6 │ │                        │ ║\n" \
       "║ ├───┼───┼───┤ │                        │ ║\n" \
       "║ │ 7 │ 8 │ 9 │ │                        │ ║\n" \
       "║ ├───┼───┼───┤ │                        │ ║\n" \
       "║ │ < │ 0 │ > │ ╰────────────────────────╯ ║\n" \
       "║ ╰───┴───┴───╯                            ║\n" \
       "║   ┌──────────────────────────────────╮   ║\n" \
       "║  ╭┤                   ╭────┰────╮    │   ║\n" \
       "║  ╞╪═══════════════════│  ┏━┻━┓  │    │   ║\n" \
       "║  ├┤                   ├─╼┫ ◯ ┣╾─┤    │   ║\n" \
       "║  ╞╪═══════════════════│  ┗━┳━┛  │    │   ║\n" \
       "║  ╰┤                   ╰────┸────╯    │   ║\n" \
       "║   └──────────────────────────────────╯   ║\n" \
       "╚══════════════════════════════════════════╝".split("\n")

intro = f"Welcome to Crack The Box, a simple, ASCII based game where you merely need to guess the code to win. At " \
        f"the end of the game, if you managed to win, you will be given a score. Your score will be lower the more " \
        f"questions and guesses you make, but will also be lower if you favour one question color over another. \n" \
        f"You can ask a question by pressing it's corresponding key, and then pressing enter. Your question-answer " \
        f"history will appear on the right, with newest questions at the top. You can scroll up and down using the q " \
        f"and w keys, respectively. \nYou can activate the numpad by pressing the e key, and then enter. Then choose " \
        f"the button you want to press and press enter again. The < is for backspace, and the > is to make a guess. " \
        f"\nQuestions have a good chance of using the current number in the Display in some way, so a good strategy " \
        f"is to always have your current guess in the Display, even if you don't make a guess with it.".split("\n")
