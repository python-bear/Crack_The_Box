import colorama as cl
from colorama import Style as st

import time

cl.init(autoreset=True)


def main(x_padding: int = 10, y_padding: int = 5, time_scale: float = 2, show_cc: bool = True):
    def clear_screen():
        print("\033[1J\033[1;1H", end="")

    def hide_cursor():
        print("\033[?25l", end="")

    def show_cursor():
        print("\033[?25h", end="")

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

    def draw(delta: int, length: float = time_scale / 25, texture: str = None):
        clear_screen()

        print("\n" * y_padding)
        for row in range(len(fl)):
            print(" " * x_padding,
                  "".join([color(fl[row][c - delta - 1]) if fl[row][c - delta - 1] != " " and row <= c <= delta + row
                           else color(texture if texture is not None and bl[row][c] != " " else bl[row][c]) for c in
                           range(len(fl[row]))]))

        time.sleep(length)

    cursor = {
        "back": "\033[1D",
        "forward": "\033[1C",
    }
    bl = """________________________________________________________        
 ________________________________________________________       
  ________________________________________________________      
   ________________________________________________________     
    ________________________________________________________    
     ________________________________________________________   
      ________________________________________________________  
       ________________________________________________________ 
        ________________________________________________________
    """.split("\n")[:-1]

    fl = r"""   21111111111111    43333333333333    655555555555             
   12111222222222111 34333444444444333 565566666666555          
    12111       12111 34333       34333 56555     56555         
     1211111111111112  3433333333333333  56555555555556         
      12111222222222    34333444444444333 56555666666555        
       12111             34333       34333 56555    566555      
        12111             34333       34333 56555     566555    
         12111             3433333333333334  56555      566555  
          1222              34444444444444    5666        5666  
    """.split("\n")[:-1]

    hide_cursor()

    for i in range(len(fl[-1])):
        draw(i)

    draw(len(fl[-1]) - 1, time_scale / 6)
    draw(len(fl[-1]) - 1, time_scale / 6, "/")
    draw(len(fl[-1]) - 1, time_scale / 6, "|")
    draw(len(fl[-1]) - 1, time_scale / 6, "\\")

    print(" " * (len(fl[-1]) - len("Python-Bear  ") + x_padding), end="", flush=True)
    for i in range(len("PBR")):
        print("PBR"[i:i + 1], end="", flush=True)
        time.sleep(0.06)

    time.sleep(time_scale / 3)
    for i in range(len("ython-")):
        print(cursor['back'] * 2, end="", flush=True)
        print(f"{'ython-'[i:i + 1]}BR", end="", flush=True)
        time.sleep(0.06)

    print(f"{cursor['back']}", end="")
    for i in range(len("ear")):
        print("ear"[i:i + 1], end="", flush=True)
        time.sleep(0.06)

    if show_cc:
        time.sleep(time_scale * 0.6)
        for i in range(len(" (CC BY-SA 4)")):
            print(f"{cursor['back']}" * (len("Python-Bear") + 1 + i), end="")
            print(f"Python-Bear{' (CC BY-SA 4)'[:i + 1]}", end="", flush=True)
            time.sleep(0.06)

        time.sleep(time_scale * 0.6)

    else:
        time.sleep(time_scale)

    clear_screen()
    show_cursor()
