#!python3

import curses
from curses.textpad import Textbox

def initscr():
    stdscr = curses.initscr()
    curses.noecho()
    return stdscr

def getuserinput(stdscr, initialtext):
    stdscr.addstr(0, 0, initialtext)
    box = Textbox(stdscr, insert_mode=True)
    def validate(ch):#handle key input
        # exit with the escape key or resize
        if ch in (27,  curses.KEY_RESIZE):
            return curses.ascii.BEL  # Control-G to exit
        # delete the character to the left of the cursor - not native with box.edit()
        elif ch in (curses.KEY_BACKSPACE, curses.ascii.DEL, curses.ascii.BS, 127):
            return curses.KEY_BACKSPACE
        return ch
    stdscr.refresh()
    box.edit(validate) # give input to user
    return box.gather().strip()#return box content

def endscr(scr):
    curses.echo()
    curses.endwin()

stdscr = initscr()
message="Inital text"
while(True):
    message = getuserinput(stdscr,message).upper()
endscr(stdscr)
