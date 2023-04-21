#!python3

import curses
import curses.textpad as textpad

def main(screen):
    """screen is a curses screen passed from the wrapper"""
    while True:
        textpad.Textbox(curses.newwin(1,13,4,0), insert_mode=True).edit()
        textpad.Textbox(curses.newwin(1,13,4,16), insert_mode=True).edit()

if __name__ == '__main__':   
    curses.wrapper(main) 