import curses
import signal
import sys
import configparser
import textwrap
from models.model_dataset import ModelDataset


class Database(object):
    def __init__(self, user, host, passwd):
        self.db = ModelDataset(user, host, passwd)
        self.db_species = self.db.list_species()
        self.db_couplets = self.db.list_couplets()
        #
        self.select_species = self.fetch_select_species()
        self.select_couplets = self.fetch_select_couplets()
        #
        self.sp_index = 0
        self.cp_index = 0

    def fetch_select_couplets(self):
        file = open('select/COUPLETS.txt').read().strip().split('\n')
        select_couplets = [c for c in self.db_couplets if c in file]
        return select_couplets

    def fetch_select_species(self):
        file = open('select/SPECIES.txt').read().strip().split('\n')
        select_species = [s for s in self.db_species if s in file]
        return select_species


def read_key(value):
    #
    r = None
    #
    curses_keys = {
    'KEY_DOWN': curses.KEY_DOWN,
    'KEY_UP': curses.KEY_UP,
    'KEY_LEFT': curses.KEY_LEFT,
    'KEY_RIGHT': curses.KEY_RIGHT,
    'KEY_BACKSPACE': curses.KEY_BACKSPACE,
    'KEY_ENTER': ord('\n')
    }
    try:
        if value in curses_keys.keys():
            r = curses_keys[value]
        else:
            r = ord(value)
    except TypeError:
        pass
    #
    return r

def read_conf():
    #
    config = configparser.ConfigParser()
    config.read('conf/conf')
    user = config['mosquito database']['User']
    host = config['mosquito database']['Host']
    passwd = config['mosquito database']['Password']
    #
    # aliasing
    nc = config['ta keybindings']['NextCouplet']
    pc = config['ta keybindings']['PreviousCouplet']
    ns = config['ta keybindings']['NextSpecies']
    ps = config['ta keybindings']['PreviousSpecies']
    u = config['ta keybindings']['Update']
    c = config['ta keybindings']['Cancel']
    q = config['ta keybindings']['Quit']
    keybindings = {
        'NextCouplet': (read_key(nc) or 's', nc),
        'PreviousCouplet': (read_key(pc) or 'a', pc),
        'NextSpecies': (read_key(ns) or 'x', ns),
        'PreviousSpecies': (read_key(ps) or 'z', ps),
        'Update': (read_key(u) or '\n', u),
        'Cancel': (read_key(c) or 'c', c),
        'Quit': (read_key(q) or 'q', q)
    }

    return user, host, passwd, keybindings

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

def main(term):
    #
    def signal_handler(sig, frame):
        ## code adapted from: https://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python
        print('You pressed Ctrl+C!')
        db.db.connection.close()
        sys.exit(0)
    #
    signal.signal(signal.SIGINT, signal_handler)
    #
    curses.curs_set(0)
    #
    term.clear()
    #
    # init color pairs
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    #
    # reading config:
    user, host, passwd, keybindings = read_conf()
    NEXT_C = keybindings['NextCouplet']
    PREV_C = keybindings['PreviousCouplet']
    NEXT_S = keybindings['NextSpecies']
    PREV_S = keybindings['PreviousSpecies']
    UPDATE = keybindings['Update']
    CANCEL = keybindings['Cancel']
    QUIT = keybindings['Quit']
    #
    # define tabspace (min of x)
    tab = 8
    #
    try:
        db = Database(user, host, passwd)
    except Exception as e:
        while True:
            term.clear()
            y, x = wrapstr(term, 2, tab, 'connection failed with following error:', curses.A_BOLD)
            y, x = wrapstr(term, y+2, tab, 'err code: {}'.format(e.args[0]), curses.color_pair(3))
            y, x = wrapstr(term, y+1, tab, 'err msg.: {}'.format(e.args[1]), curses.color_pair(3))
            y, x = wrapstr(term, y+2, tab, 'contact your database admin')
            y, x = wrapstr(term, y+1, tab, 'press any key to exit')
            key = term.getch()
            if key == curses.KEY_RESIZE:
                continue
            else:
                return
    #
    while True:
        term.clear()
        #
        couplet = db.select_couplets[db.cp_index]
        zero_text, one_text = db.db.show_couplet(couplet)
        species = db.select_species[db.sp_index]
        status = db.db.show_state(species, couplet)
        #
        y, x = wrapstr(term, 2, tab, 'current couplet: {}'.format(couplet))
        y, x = wrapstr(term, y+2, tab+4, '0. {}'.format(zero_text))
        y, x = wrapstr(term, y+2, tab+4, '1. {}'.format(one_text))
        y, x = wrapstr(term, y+2, tab, 'current species: {}'.format(species))
        y, x = wrapstr(term, y+2, tab+4, 'status: {}'.format(status))
        #
        # freeze input y pos
        input_y = y+2
        #
        # display helper text
        y, x = wrapstr(term, y+7, tab, 'keybindings:', curses.A_DIM)
        y, x = wrapstr(term, y+1, tab, '({}) previous couplet  ({}) next couplet      ({}) update'.format(PREV_C[1], NEXT_C[1], UPDATE[1]), curses.A_DIM)
        y, x = wrapstr(term, y+1, tab, '({}) previous species  ({}) next species      ({}) quit'.format(PREV_S[1], NEXT_S[1], QUIT[1]), curses.A_DIM)
        #
        key = term.getch()
        #
        if key == NEXT_C[0]:
            if db.cp_index < len(db.select_couplets):
                db.cp_index += 1
        elif key == PREV_C[0]:
            if db.cp_index > 0:
                db.cp_index -= 1
        elif key == NEXT_S[0]:
            if db.sp_index < len(db.select_species):
                db.sp_index += 1
        elif key == PREV_S[0]:
            if db.sp_index > 0:
                db.sp_index -= 1
        elif key == UPDATE[0]:
            y, x = wrapstr(term, input_y, tab, 'type a new value to edit the database:   ')
            curses.curs_set(1)
            curses.echo()
            new_status = term.getstr(y, x+1).decode('utf-8').upper()
            curses.noecho()
            curses.curs_set(0)
            if new_status.upper() == 'NULL_VALUE':
                new_status = None
            if new_status in ['0', '1', '01', '10', 'NA', None]:
                y, x = wrapstr(term, y+1, tab, 'new status: {}'.format(new_status), curses.A_BOLD)
                y, x = wrapstr(term, y+1, tab, "press any key to confirm, '{}' to cancel".format(CANCEL[1]))
                confirm = term.getch()
                if confirm == CANCEL[0]:
                    y, x = wrapstr(term, y+1, tab, 'action cancelled, press any key to continue', curses.color_pair(3))
                else:
                    db.db.update(species, new_status, couplet)
                    y, x = wrapstr(term, y+1, tab, 'change confirmed, press any key to continue', curses.color_pair(2))
            else:
                y, x = wrapstr(term, y+1, tab, 'illegal status: {}, type({})'.format(new_status, type(new_status)), curses.color_pair(3))
                y, x = wrapstr(term, y+1, tab, "please type '0', '1', '01' or 'NA'")
            term.getch()
        elif key == QUIT[0]:
            break
        elif key == curses.KEY_RESIZE:
            pass

    db.db.connection.close()


if __name__ == '__main__':
    curses.wrapper(main)
