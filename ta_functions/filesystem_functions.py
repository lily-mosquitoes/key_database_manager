import os
import sys
import curses


def get_file(term, path, type, message):

    curses.curs_set(0)

    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_MAGENTA)

    max_lines = 10
    max_cols = 60

    term.clear()

    term.addstr(1, 1, message)

    rectangle = term.subwin(max_lines+2, max_cols+2, 2, 1)

    fileswin = rectangle.subwin(max_lines+1, max_cols, 3, 2)

    cursor = 0
    line_start = 0

    while True:
        #
        dir_files = [f for f in os.listdir(path) if not f.startswith('.')]
        #
        fileswin.clear()
        rectangle.border()
        #
        y = x = 0
        for file in dir_files[line_start:line_start+max_lines]:
            if y == cursor:
                fileswin.addstr(y, x, file, curses.color_pair(4))
            else:
                fileswin.addstr(y, x, file)
            y += 1

        term.refresh()
        rectangle.refresh()
        fileswin.refresh()

        key = term.getch()

        if key == curses.KEY_DOWN:
            if (cursor == max_lines-1 and line_start+max_lines == len(dir_files)) or cursor == len(dir_files)-1:
                pass
            else:
                if cursor == max_lines-1:
                    line_start += 1
                else:
                    cursor += 1

        elif key == curses.KEY_UP:
            if line_start == 0 and cursor == 0:
                pass
            else:
                if cursor == 0:
                    line_start -= 1
                else:
                    cursor -= 1

        elif key == curses.KEY_RIGHT:
            new_path = dir_files[line_start:line_start+max_lines][cursor]
            new_path = os.path.join(path, new_path)
            if os.path.isdir(new_path):
                path = new_path
                cursor = 0
                line_start = 0

        elif key == curses.KEY_LEFT:
            path = os.path.abspath(os.path.dirname(path))
            cursor = 0
            line_start = 0

        elif key == ord('q'): # 27 is the ESC key
            return ''

        elif key == ord('\n'):
            new_path = dir_files[line_start:line_start+max_lines][cursor]
            new_path = os.path.join(path, new_path)
            if os.path.isfile(new_path) and new_path.endswith(type):
                return new_path
            elif os.path.isdir(new_path):
                path = new_path
                cursor = 0
                line_start = 0
