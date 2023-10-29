from bin.ascii import *
from bin.numbering import *

import os
import time
import msvcrt


def get_key():
    key = msvcrt.getch()
    return key


class Game:
    def __init__(self, height: int = 29, width: int = 100):
        self.title = f"{fg.RED}{st.BRIGHT} _____                _      _____ _           ______           \n/  __ *  " \
                     f"            | |    |_   _| |          | ___ *          \n| /  */_ __ __ _  ___| | __   | | | |" \
                     f"__   ___  | |_/ / _____  __\n| |   | '__/ _` |/ __| |/ /   | | | '_ * / _ * | ___ */ _ * */ /" \
                     f"\n| *__/* | | (_| | (__|   <    | | | | | |  __/ | |_/ / (_) >  < \n*_____/_|  *__,_|*___|_|*_" \
                     f"*   *_/ |_| |_|*___| *____/ *___/_/*_*{st.RESET_ALL}\n".replace("*", "\\")
        self.canvas = [[" " for w in range(width)] for h in range(height)]
        self.h = height
        self.w = width
        self.keys = "ASDF"
        self.scroll_keys = "QW"

        self.debug = False
        self.selected = None
        self.animation_index = 0
        self.score = 1000
        self.selected_numpad = "0"
        self.game_over = False
        self.state = "normal"
        self.low = 9999
        self.top = 0
        self.num = random.randint(self.top, self.low)
        self.curr_num = 0000
        self.history = []
        self.history_surf = None
        self.history_view = (0, 20)  # min, max
        self.stats = {
            "magenta": 0,
            "green": 0,
            "blue": 0,
            "yellow": 0,
            "questions": 0,
            "guesses": 0,
        }
        self.questions = self.gen_questions()

        self.colors = {
            "fg": {
                "yellow": fg.YELLOW,
                "blue": fg.BLUE,
                "magenta": fg.MAGENTA,
                "green": fg.GREEN,
                "True": fg.CYAN,
                "False": fg.RED,
                "Yes": fg.CYAN,
                "No": fg.RED,
                "questions": fg.RED,
                "guesses": fg.CYAN,
                "white": fg.WHITE

            },
            "bg": {
                "yellow": bg.YELLOW,
                "blue": bg.BLUE,
                "magenta": bg.MAGENTA,
                "green": bg.GREEN,
                "True": bg.CYAN,
                "False": bg.RED,
                "Yes": bg.CYAN,
                "No": bg.RED,
                "questions": bg.RED,
                "guesses": bg.CYAN,
                "white": bg.WHITE
            }
        }

    def run(self):
        hide_cursor()

        while not self.game_over:
            self.render()
            self.update()
            time.sleep(0.02)

        show_cursor()
        os.system("exit")

    def update(self):
        if self.stats["questions"] > 40:
            self.game_failure("questions", 40)
            return
        elif self.stats["guesses"] > 10:
            self.game_failure("guesses", 10)
            return

        if self.questions is None:
            self.questions = self.gen_questions()

        try:
            action = get_key().decode('utf-8').upper()
        except UnicodeDecodeError:
            action = ""

        if action in "0123456789<>":
            self.selected_numpad = action

        else:
            if action in self.keys:
                self.selected = action
                self.state = "normal"
            elif action == "E":
                self.selected = action
                self.state = "normal"
            elif action in "\r\n":
                if self.state == "numpad":
                    if self.selected_numpad in "0123456789":
                        if self.curr_num == 0:
                            self.curr_num = self.selected_numpad
                        else:
                            self.curr_num = int(f"{str(self.curr_num)[:3]}{self.selected_numpad}")
                    elif self.selected_numpad in "<,":
                        try:
                            self.curr_num = int(str(self.curr_num)[:-1])
                        except ValueError:
                            self.curr_num = 0
                    elif self.selected_numpad in ">.":
                        self.guess_number()
                elif self.state == "normal":
                    if self.selected == "E":
                        self.state = "numpad"
                    elif self.selected is not None:
                        self.state = "normal"
                        self.choose_question(self.questions[self.keys.index(self.selected)])
            elif self.history is not None and self.history_surf is not None:
                if action == self.scroll_keys[0] and self.history_view[0] - 1 >= 0:
                    self.history_view = [self.history_view[0] - 1, self.history_view[1] - 1]
                    self.state = "normal"
                elif action == self.scroll_keys[1] and self.history_view[1] + 1 <= len(self.history_surf):
                    self.history_view = [self.history_view[0] + 1, self.history_view[1] + 1]
                    self.state = "normal"

    def render(self, won: bool = False):
        clear_screen()
        self.canvas = erase(self.canvas)

        if self.debug:
            print(self.title + str(self.num) + "\n")
        else:
            print(self.title + "\n")

        curr_num = str(self.curr_num).rjust(4, "0")[::-1]
        for col, digit in enumerate(curr_num):
            for row, segment in enumerate(segment_digits[digit]):
                self.canvas[row + 2][self.w - ((col + 1) * segment_digits["w"]) - 3:
                                     self.w - col * segment_digits["w"] - 3] = segment

        if self.state == "numpad":
            self.canvas = blit(self.canvas, color_lines(safe, self.selected_numpad, bg.CYAN),
                               (0, self.w - len(safe[0])))
        else:
            self.canvas = blit(self.canvas, safe, (0, self.w - len(safe[0])))

        for j, stat in enumerate(self.stats.keys()):
            self.canvas[9][self.w - len(safe[0]) + 17 + j * 4] = self.colors["bg"][stat] + stat[0].upper() + \
                                                                 st.RESET_ALL
            self.canvas[9][self.w - len(safe[0]) + 17 + j * 4 + 1] = self.colors["fg"][stat] + ":" + st.RESET_ALL

            for i, char in enumerate(str(self.stats[stat])):
                self.canvas[9][self.w - len(safe[0]) + 17 + j * 4 + 2 + i] = \
                    self.colors["fg"][stat] + char + st.RESET_ALL

        if self.questions is not None:
            for i, question in enumerate(self.questions):
                self.canvas[len(safe) + i + 1][self.w - len(safe[0])] = \
                    self.colors["bg"][str(question[1])] + self.keys[i] + st.RESET_ALL
                self.canvas[len(safe) + i + 1][self.w - len(safe[0]) + 1] = \
                    ". " + self.colors["fg"][str(question[1])] + question[0] + st.RESET_ALL

            for i, key in enumerate(self.keys):
                self.canvas[1][(i + 1) * 5] = self.colors["bg"][str(self.questions[i][1])] + key + st.RESET_ALL if \
                    self.selected == key else \
                    self.colors["fg"][str(self.questions[i][1])] + key + st.RESET_ALL

            self.canvas[1][(len(self.keys) + 1) * 5] = bg.CYAN + "E" + st.RESET_ALL if \
                self.selected == "E" else fg.CYAN + "E" + st.RESET_ALL

            if self.selected is not None and self.selected != "E":
                lines = self.questions[self.keys.index(self.selected)][0]
                lines = word_wrap(lines, self.w - len(safe[0]) - 6)
                if len(lines) == 1:
                    lines.append(" ")
                lines = [f"{lines[i]}{' ' * ((self.w - len(safe[0])) - (len(lines[0]) + 6))}" for i in
                         range(len(lines))]

                for j, line in enumerate(lines):
                    for i, char in enumerate(line):
                        self.canvas[3 + j][i + 6] = char + st.RESET_ALL if i == len(line) - 1 else \
                            self.colors["fg"][str(self.questions[self.keys.index(self.selected)][1])] + char if i == 0 \
                            else char

            if len(self.history) != 0 and not won:
                try:
                    self.history_surf = [[" " for w in range(self.w - len(safe[0]) - 6)] for h in range(1)]
                    row = 0
                    for y in range(len(self.history[::-1])):
                        lines = self.history[::-1][y][0]
                        lines = word_wrap(lines, self.w - len(safe[0]) - 6)
                        lines = [f"{lines[i]}{' ' * ((self.w - len(safe[0])) - (len(lines[0]) + 6))}" for i in
                                 range(len(lines))]

                        answer = f"    {self.history[::-1][y][-1]}"

                        for _ in range(1 + len(lines)):
                            self.history_surf.append([" " for w in range(self.w - len(safe[0]) - 6)])

                        for j, line in enumerate(lines):
                            for i, char in enumerate(line):
                                self.history_surf[row + j][i] = char + st.RESET_ALL if i == len(line) - 1 else \
                                    fg.WHITE + char if i == 0 else char
                            row += j

                        for i, char in enumerate(answer):
                            self.history_surf[row + 1][i] = char + st.RESET_ALL if i == len(answer) - 1 else \
                                self.colors["fg"].get(str(self.history[::-1][y][-1]), fg.RED) + char if \
                                i == 0 else char
                        row += 2
                except:
                    pass

                self.canvas = blit(self.canvas, self.history_surf[self.history_view[0]:self.history_view[1]], (7, 6))

            elif self.selected is None:
                r = 0
                for paragraph in intro:
                    lines = word_wrap(paragraph, self.w - len(safe[0]) - 6)

                    for line in lines:
                        for i, char in enumerate(line):
                            self.canvas[r + 3][i + 1] = char
                        r += 1

                    r += 1

        if won:
            won_str = f"Your final score is: "
            redaction = 0
            form = None

            for i, char in enumerate(won_str):
                self.canvas[7][i + 6] = char

                if i == len(won_str) - 1:
                    for j in range(len(str(self.score))):
                        self.canvas[7][j + 6 + len(won_str)] = st.BRIGHT + fg.CYAN + str(self.score)[j] + st.RESET_ALL

            if self.animation_index == 1:
                redaction = (self.stats["guesses"] - 1) * 15 - (0 if self.stats["guesses"] == 1 else 5)
                form = "guesses"
            elif self.animation_index == 2:
                redaction = self.stats["magenta"] * 14
                form = "magenta"
            elif self.animation_index == 3:
                redaction = self.stats["green"] * 14
                form = "green"
            elif self.animation_index == 4:
                redaction = self.stats["blue"] * 14
                form = "blue"
            elif self.animation_index == 5:
                redaction = self.stats["yellow"] * 14
                form = "yellow"
            elif self.animation_index == 6:
                redaction = variation([self.stats["magenta"], self.stats["green"], self.stats["yellow"],
                                       self.stats["blue"]]) * 2
                form = "white"
            redaction = int(redaction)
            self.score -= redaction
            self.animation_index += 1

            if form is not None:
                for j in range(len(minusise(redaction))):
                    self.canvas[8][j + 6 + len(won_str)] = self.colors["fg"][form] + \
                                                           minusise(redaction)[j] + st.RESET_ALL

        for row in self.canvas:
            print("".join(row).rstrip())

    def ask_to_replay(self, won: bool = False):
        self.questions = [["Would you like to play again?", True, True],
                          ["Would you like to stop playing?", False, False],
                          ["Would you like to play again?", True, True],
                          ["Would you like to stop playing?", False, False]]
        self.state = "normal"
        self.curr_num = self.num

        if won:
            while self.animation_index < 7:
                self.render(won)
                time.sleep(1.5)

        while True:
            self.render(won)

            try:
                action = get_key().decode('utf-8').upper()
            except UnicodeDecodeError:
                action = ""

            if action in self.keys:
                self.selected = action
            elif action in "\r\n":
                if self.selected in (self.keys[0], self.keys[2]):
                    self.reset_game()
                    return
                elif self.selected in (self.keys[1], self.keys[3]):
                    self.game_over = True
                    return

    def game_failure(self, reason, high):
        self.history.append([f"You have reached the maximum number of {reason}, which is {high}. The number was "
                             f"{self.num}", False, "Failure"])
        self.ask_to_replay()

    def guess_number(self):
        self.stats["guesses"] += 1
        if self.curr_num == self.num:
            self.history.append([f"Is the password {self.curr_num}?", "white", True])

            self.ask_to_replay(True)

        else:
            delta = max(int(self.num), int(self.curr_num)) - min(int(self.num), int(self.curr_num))
            message = random.choice(("Your guess is", "You're"))
            if delta > 9500:
                clue = f"{message} as bad as one can get."
            elif delta > 8999:
                clue = f"{message} excruciatingly far {random.choice(('off', 'away'))}."
            elif delta > 7499:
                clue = f"{message} remarkably far {random.choice(('off', 'away'))}."
            elif delta > 7000:
                clue = f"{message} extremely far {random.choice(('off', 'away'))}."
            elif delta > 6500:
                clue = f"{message} nowhere close."
            elif delta > 6000:
                clue = f"{message} far {random.choice(('off', 'away'))}."
            elif delta > 5500:
                clue = f"{message} just worse than random."
            elif delta > 4998:
                clue = f"{message} as good as random."
            elif delta > 4400:
                clue = f"{message} somewhat better than random."
            elif delta > 4000:
                clue = f"{message} passably close."
            elif delta > 3000:
                clue = f"{message} somewhat close."
            elif delta > 2000:
                clue = f"{message} moderately close."
            elif delta > 1000:
                clue = f"{message} reasonably close."
            elif delta > 800:
                clue = f"{message} rather close."
            elif delta > 500:
                clue = f"{message} fairly close."
            elif delta > 100:
                clue = f"{message} quite close."
            elif delta > 75:
                clue = f"{message} pretty close."
            elif delta > 50:
                clue = f"{message} considerably close."
            elif delta > 20:
                clue = f"{message} very close."
            elif delta > 10:
                clue = f"{message} extremely close."
            elif delta > 5:
                clue = f"{message} almost excruciatingly close."
            elif delta > 3:
                clue = f"{message} excruciatingly close."
            elif delta >= 2:
                clue = f"{message} very excruciatingly close."
            elif delta <= 1:
                clue = f"{message} one off."

            self.history.append([f"Is the password {self.curr_num}?", "white", clue])

    def choose_question(self, question):
        self.history.append([question[0], question[1], "Yes" if question[2] else "No"])
        self.selected = None
        try:
            self.stats[question[1]] += 1
        except KeyError:
            pass
        self.stats["questions"] += 1
        self.questions = self.gen_questions()
        self.render()

    def gen_questions(self):
        questions = []

        for _ in range(4):
            curr_question = [[], [], []]  # question, color, answer
            seed = [random.randint(0, 22), random.randint(self.top, self.low), random.randint(0, 10)]
            it = ("it", self.num) if is_even(seed[-1]) or is_prime(seed[-1]) else \
                ("a certain number next to it", deviate(self.num)) if seed[-1] <= 15 else \
                    ("a certain number up to two away from it", deviate(self.num, 2))
            color_id = random.choice(["yellow", "blue", "magenta", "green"])

            if self.curr_num not in [0, 9999]:
                num = random.choice([self.curr_num, seed[1]])
            else:
                num = seed[1]

            if seed[0] in (0, 10):
                curr_question = [f"Is {it[0]} even?", color_id, is_even(it[-1])]
            elif seed[0] in (1, 11):
                curr_question = [f"Is {it[0]} odd?", color_id, is_odd(it[-1])]
            elif seed[0] in (2, 3, 4, 5):
                comp = random.choice([">", "<", ">=", "<="])
                curr_question = [f"Is {it[0]} {wordify[comp]} {num}?", color_id, eval(f"{it[-1]} {comp} {num}")]
            elif seed[0] == 6:
                curr_question = [f"Is {it[0]} a prime?", color_id, is_prime(it[-1])]
            elif seed[0] == 7:
                curr_question = [f"Is {it[0]} a perfect number?", color_id, is_perfect(it[-1])]
            elif seed[0] == 8:
                curr_question = [f"Is {it[0]} palindromic?", color_id, is_palindromic(it[-1])]
            elif seed[0] == 9:
                curr_question = [f"Is {it[0]} a square number?", color_id, is_square(it[-1])]
            elif seed[0] == 9:
                curr_question = [f"Is {it[0]} in the Fibonacci sequence?", color_id, is_square(it[-1])]
            elif seed[0] == 9:
                num = int(it[-1] * random.choice((1, 1.5, 2, 2.25, 2.5, 3, 3.5, 4, 4.5, 5, 5.5)))
                curr_question = [f"Is {it[0]} a factor of {num}?", color_id, is_factor(it[-1], num)]
            elif seed[0] == 12:
                num = it[-1] // random.choice((1, 1.5, 2, 2.25, 2.5, 3, 3.5, 4, 4.5, 5, 5.5))
                curr_question = [f"Is {int(num)} a factor of {it[0]}?", color_id, is_factor(num, it[-1])]
            elif seed[0] == 13:
                num = find_multiples(it[-1], self.top, self.low)
                if len(num) in (0, 1):
                    digit = str(random.randint(0, 9))
                    curr_question = [f"Does {it[0]} end in {digit}?", color_id,
                                     str(it[-1])[::-1][-1] == digit]
                else:
                    num = random.choice(num)
                    curr_question = [f"Is {it[0]} a multiple of {num}?", color_id, is_multiple(it[-1], num)]
            elif seed[0] == 14:
                num = find_multiples(it[-1], self.top, self.low)
                if len(num) in (0, 1):
                    digit = str(random.randint(0, 9))
                    curr_question = [f"Does {it[0]} start with {digit}?", color_id,
                                     str(it[-1])[::-1][0] == digit]
                else:
                    num = random.choice(num)
                    curr_question = [f"Is {num} a multiple of {it[0]}?", color_id, is_multiple(num, it[-1])]
            elif seed[0] == 15:
                percent = random.randint(0, 100)
                curr_question = [f"Is {it[0]} within {percent}% of {num}?", color_id,
                                 is_within(it[-1], int(num), int(percent_of(percent, self.low)))]
            elif seed[0] == 16:
                digit = str(random.choice((*range(0, 9), str(it[-1])[-1])))
                curr_question = [f"Does {it[0]} end in {digit}?", color_id,
                                 str(it[-1])[-1] == digit]
            elif seed[0] == 17:
                digit = str(random.choice((*range(0, 9), str(it[-1])[0])))
                curr_question = [f"Does {it[0]} start with {digit}?", color_id,
                                 str(it[-1])[0] == digit]
            elif seed[0] == 18:
                digit = str(random.choice((*range(0, 9), str(it[-1])[1])))
                curr_question = [f"Is {it[0]}'s second digit {digit}?", color_id,
                                 str(it[-1])[1] == digit]
            elif seed[0] == 19:
                digit = str(random.choice((*range(0, 9), str(it[-1])[2])))
                curr_question = [f"Is {it[0]}'s third digit {digit}?", color_id,
                                 str(it[-1])[2] == digit]
            elif seed[0] == 20:
                delta = random.randint(0, 4900)
                curr_question = [f"Is {it[0]} within {delta} of {num}?", color_id,
                                 is_within(it[-1], int(num), int(delta))]
            elif seed[0] == 21:
                if num == self.curr_num:
                    area = sorted((
                        abs(random.randint(
                            int(num - percent_of(random.randint(1, 49), self.low)),
                            int(num + percent_of(random.randint(1, 49), self.low)))),

                        abs(random.randint(
                            int(num - percent_of(random.randint(1, 49), self.low)),
                            int(num + percent_of(random.randint(1, 49), self.low))))
                    ))
                else:
                    area = (random.randint(self.top, self.low), random.randint(self.top, self.low))
                    area = (min(area), max(area))
                curr_question = [f"Is {it[0]} between {area[0]} and {area[1]}?", color_id, it[-1] in range(*area)]
            elif seed[0] == 22:
                if num == self.curr_num:
                    area = sorted((
                        abs(random.randint(
                            int(num - percent_of(random.randint(1, 49), self.low)),
                            int(num + percent_of(random.randint(1, 49), self.low)))),

                        abs(random.randint(
                            int(num - percent_of(random.randint(1, 49), self.low)),
                            int(num + percent_of(random.randint(1, 49), self.low))))
                    ))
                else:
                    area = (random.randint(self.top, self.low), random.randint(self.top, self.low))
                    area = (min(area), max(area))
                curr_question = [f"Is {it[0]} not between {area[0]} and {area[1]}?", color_id, not it[-1] in
                                 range(*area)]

            questions.append(curr_question)
        return questions

    def reset_game(self):
        self.canvas = [[" " for w in range(self.w)] for h in range(self.h)]
        self.selected = None
        self.animation_index = 0
        self.score = 1000
        self.selected_numpad = "0"
        self.game_over = False
        self.state = "normal"
        self.low = 9999
        self.top = 0
        self.num = random.randint(self.top, self.low)
        self.curr_num = 0000
        self.history = []
        self.history_surf = None
        self.history_view = (0, 20)  # min, max
        self.stats = {
            "magenta": 0,
            "green": 0,
            "blue": 0,
            "yellow": 0,
            "questions": 0,
            "guesses": 0,
        }
        self.questions = self.gen_questions()
