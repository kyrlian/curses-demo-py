#!python3

import curses
from curses.textpad import Textbox


def initscr():
    stdscr = curses.initscr()
    curses.noecho()
    return stdscr


def endscr(scr):
    curses.echo()
    curses.endwin()


def addinputbox(parentwin, initialtext):
    # with derwin, begin is relative to parent window
    inputwin = parentwin.derwin(
        parentwin.getmaxyx()[0]-2, parentwin.getmaxyx()[1]-2, 1, 1)
    inputwin.addstr(0, 0, initialtext)
    box = Textbox(inputwin, insert_mode=True)

    def validate(ch):  # handle key input
        # exit with the escape key or resize
        # if ch in (27,  curses.KEY_RESIZE):
        if ch == 27:
            return curses.ascii.BEL  # Control-G to exit
        # delete the character to the left of the cursor - not native with box.edit()
        elif ch in (curses.KEY_BACKSPACE, curses.ascii.DEL, curses.ascii.BS, 127):
            return curses.KEY_BACKSPACE
        return ch
    parentwin.refresh()
    box.edit(validate)  # give input to user
    return box.gather().strip()  # return box content


def addtitle(win, title):
    win.addstr(0, 1, title)
    return win


def addtext(win, text):
    win.addstr(1, 1, text)
    return win


def addsubwin(parentwin, startxpct=0, startypct=0, widthpct=1, heightpct=1,title=None, text=None):
    (parentrows, parentcols) = parentwin.getmaxyx()
    beginrow = int(parentrows * startypct)
    if startypct >= 1:
        beginrow = startypct
    begincol = int(parentcols * startxpct)
    if startxpct >= 1:
        begincol = startxpct
    newwinrows = int(parentrows * heightpct)
    if heightpct > 1:
        newwinrows = heightpct
    newwinrows = min(newwinrows, parentrows-beginrow)
    newwincols = int(parentcols * widthpct)
    if widthpct > 1:
        newwincols = widthpct
    newwincols = min(newwincols, parentcols-begincol)
    # newwin = parentwin.subwin(newwinrows, newwincols, beginrow, begincol) #with subwin, begin is relative to whole screen
    # with derwin, begin is relative to parent window
    newwin = parentwin.derwin(newwinrows, newwincols, beginrow, begincol)
    newwin.border()
    if title is not None:
        addtitle(newwin, title)
    if text is not None:
        addtext(newwin, text)
    newwin.refresh()
    return newwin


def addfloatingwin(lines, cols, beginline, begincol, title=None, text=None):
    floatingwin = curses.newwin(lines, cols, beginline, begincol)
    floatingwin.border()
    if title is not None:
        addtitle(floatingwin, title)
    if text is not None:
        addtext(floatingwin, text)
    floatingwin.refresh()
    return floatingwin


def addbutton(parentwin, row,col,text, callback):
    buttonwin = parentwin.derwin(3, len(text)+2, row, col)
    buttonwin.border()
    buttonwin.addstr(1, 1, text)
    buttonwin.refresh()
    return buttonwin

def button1action():
    print("a")

def activatebuttons(buttonlist):#TODO: to call that on event
    (id, x, y, z, bstate) = curses.getmouse()
    for buttonwin,callback in buttonlist:
        if buttonwin.enclose(x,y):
            callback()

def main(screen):
    topwin = addsubwin(screen, 0, 0, 1, .4,"Top win title", "Top win text")
    leftlowwin = addsubwin(screen, 0, 0.4, .7, 1,"Interactive Box")
    rightlowwin = addsubwin(screen,.7,.4,title="Menu")
    button1 = addbutton(rightlowwin,1,4,"Action1",button1action)
    buttonlist=[]
    buttonlist.append((button1,button1action))
    #floatingwin = addfloatingwin(3, 10, int(screen.getmaxyx()[0]/2), int(screen.getmaxyx()[1]/2), "floating", "text")
    userinput = addinputbox(leftlowwin, "Type here")

#screen = initscr()
curses.wrapper(main) 
#endscr(screen)
