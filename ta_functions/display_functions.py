import curses
import textwrap


def wrapstr(term, y, x, text, format=0):
    lines, cols = term.getmaxyx()
    wrapped = textwrap.wrap(text, cols-1-x)
    if y + len(wrapped) < lines-1:
        for line in wrapped:
            term.addstr(y, x, line, format)
            y += 1
    else:
        pass
    return term.getyx()

def get_text(term, y, x, message, field, password=False):

    line = y
    tab = x

    max_lines = 1
    max_cols = 60

    rectangle = term.subwin(max_lines+2, max_cols+2, line+3, tab)

    editwin = rectangle.subwin(max_lines+1, max_cols, line+4, tab+1)

    cursor = 0
    line_start = 0

    while True:

        term.clear()

        y, x = wrapstr(term, line, tab, message, curses.A_BOLD)

        y, x = wrapstr(term, line+2, tab, field)

        editwin.clear()
        rectangle.border()

        term.refresh()
        rectangle.refresh()
        editwin.refresh()

        curses.curs_set(1)
        if not password:
            curses.echo()
        text = editwin.getstr(0, 0).decode('utf-8')
        curses.noecho()
        curses.curs_set(0)

        if password:
            display_text = '•'*len(text)
        else:
            display_text = text

        y, x = wrapstr(term, y+2, tab, 'confirm {} as {}?'.format(field, display_text))
        y, x = wrapstr(term, y+1, tab, 'press ENTER to confirm, press any other key to cancel')

        key = term.getch()

        if key == ord('\n'):
            return text

def readkey(key_number):
    alias_keys = {
        curses.KEY_UP: 'UP',
        curses.KEY_DOWN: 'DOWN',
        curses.KEY_LEFT: 'LEFT',
        curses.KEY_RIGHT: 'RIGHT',
        curses.KEY_BACKSPACE: 'BACKSPACE',
        ord('\n'): 'ENTER',
        ord(' '): 'SPACE',
        ord('\t'): 'TAB'
    }
    if key_number in alias_keys.keys():
        key_name = alias_keys[key_number]
    else:
        key_name = chr(key_number)
    return key_name
