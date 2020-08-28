import curses
import signal
import sys
import os
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
        file = open(os.path.join(os.path.dirname(sys.argv[0]), 'select', 'COUPLETS.txt')).read().strip().split('\n')
        select_couplets = [c for c in self.db_couplets if c in file]
        return select_couplets

    def fetch_select_species(self):
        file = open(os.path.join(os.path.dirname(sys.argv[0]), 'select', 'SPECIES.txt')).read().strip().split('\n')
        select_species = [s for s in self.db_species if s in file]
        return select_species

    def signal_handler(self, sig, frame):
        self.db.connection.close()
        sys.exit(0)


###
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

def set_config_data(term, config, config_path):
    #
    tab = 8
    if config.has_section('mosquito database'):
        pass
    else:
        config.add_section('mosquito database')
    for i in ['User', 'Host', 'Password']:
        term.clear()
        y, x = wrapstr(term, 4, tab, 'please configure your User, Host and Password', curses.A_BOLD)
        y, x = wrapstr(term, y+1, tab, "please don't resize this window", curses.A_DIM)
        # get user
        y, x = wrapstr(term, y+2, tab, "type the '{}' and press ENTER:".format(i))
        curses.curs_set(1)
        if i != 'Password':
            curses.echo()
        value = term.getstr(y, x+1).decode('utf-8')
        curses.noecho()
        curses.curs_set(0)
        config.set('mosquito database', i, value)
    #
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def set_config_keybindings(term, config, config_path):
    #
    tab = 8
    if config.has_section('keybindings'):
        pass
    else:
        config.add_section('keybindings')
    for i in [('NextCouplet', 's'), ('PreviousCouplet', 'a'), ('NextSpecies', 'x'), ('PreviousSpecies', 'z'), ('Update', 'ENTER'), ('Confirm', 'ENTER'), ('Quit', 'q')]:
        term.clear()
        y, x = wrapstr(term, 4, tab, 'please configure your key bindings', curses.A_BOLD)
        y, x = wrapstr(term, y+1, tab, "please don't resize this window", curses.A_DIM)
        # get user
        y, x = wrapstr(term, y+2, tab, "please press a key for '{}' (suggested key: '{}')".format(i[0], i[1]))
        key = term.getch()
        config.set('keybindings', i[0], str(key))
    #
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def read_config(term, config_path):
    #
    config = configparser.ConfigParser()
    try:
        config.read(config_path)
        user = config.get('mosquito database', 'User')
        host = config.get('mosquito database', 'Host')
        passwd = config.get('mosquito database', 'Password')
    except Exception:
        set_config_data(term, config, config_path)
        config.read(config_path)
        user = config.get('mosquito database', 'User')
        host = config.get('mosquito database', 'Host')
        passwd = config.get('mosquito database', 'Password')
    try:
        config.read(config_path)
        keybindings = {
            'NextCouplet': int(config.get('keybindings', 'NextCouplet')),
            'PreviousCouplet': int(config.get('keybindings', 'PreviousCouplet')),
            'NextSpecies': int(config.get('keybindings', 'NextSpecies')),
            'PreviousSpecies': int(config.get('keybindings', 'PreviousSpecies')),
            'Update': int(config.get('keybindings', 'Update')),
            'Confirm': int(config.get('keybindings', 'Confirm')),
            'Quit': int(config.get('keybindings', 'Quit'))
        }
    except Exception:
        set_config_keybindings(term, config, config_path)
        config.read(config_path)
        keybindings = {
            'NextCouplet': int(config.get('keybindings', 'NextCouplet')),
            'PreviousCouplet': int(config.get('keybindings', 'PreviousCouplet')),
            'NextSpecies': int(config.get('keybindings', 'NextSpecies')),
            'PreviousSpecies': int(config.get('keybindings', 'PreviousSpecies')),
            'Update': int(config.get('keybindings', 'Update')),
            'Confirm': int(config.get('keybindings', 'Confirm')),
            'Quit': int(config.get('keybindings', 'Quit'))
        }
    #
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

def connection_error_handler(term, e):
    tab = 8
    while True:
        term.clear()
        y, x = wrapstr(term, 2, tab, 'connection failed with following error:', curses.A_BOLD)
        y, x = wrapstr(term, y+2, tab, 'err code: {}'.format(e.args[0]), curses.color_pair(3))
        y, x = wrapstr(term, y+1, tab, 'err msg.: {}'.format(e.args[1]), curses.color_pair(3))
        y, x = wrapstr(term, y+2, tab, 'contact your database admin')
        y, x = wrapstr(term, y+1, tab, 'press any key to exit')
        key = term.getch()
        if key == curses.KEY_RESIZE:
            continue # this deals with resizing the terminal window
        else:
            sys.exit(0)

def main(term):
    # define tabspace (min of x)
    tab = 8
    #
    # hide cursor
    curses.curs_set(0)
    #
    # clear terminal
    term.clear()
    #
    # init color pairs
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    #
    # config path
    config_path = os.path.join(os.path.dirname(sys.argv[0]), 'config', 'ta_key_data_manager.config')
    #
    # confirm configuration
    while True:
        term.clear()
        # reading config
        user, host, passwd, keybindings = read_config(term, config_path)
        NEXT_C = keybindings['NextCouplet']
        PREV_C = keybindings['PreviousCouplet']
        NEXT_S = keybindings['NextSpecies']
        PREV_S = keybindings['PreviousSpecies']
        UPDATE = keybindings['Update']
        CONFIRM = keybindings['Confirm']
        QUIT = keybindings['Quit']
        #
        y, x = wrapstr(term, 2, tab, "Please press any key to confirm your user configuration; press 'r' to reset database login configuration, or press 't' to reset your keybindings", curses.A_BOLD)
        #
        # show database config
        y, x = wrapstr(term, y+2, tab, 'user: {}'.format(user))
        y, x = wrapstr(term, y+2, tab, 'host: {}'.format(host))
        y, x = wrapstr(term, y+2, tab, 'passwd: {}'.format('-'*len(passwd)))
        #
        # show keybindings config
        y, x = wrapstr(term, y+7, tab, 'this is your current keybindings configuration:', curses.A_DIM)
        y, x = wrapstr(term, y+1, tab, '({}) previous couplet  ({}) next couplet      ({}) update'.format(readkey(PREV_C), readkey(NEXT_C), readkey(UPDATE)), curses.A_DIM)
        y, x = wrapstr(term, y+1, tab, '({}) previous species  ({}) next species      ({}) quit'.format(readkey(PREV_S), readkey(NEXT_S), readkey(QUIT)), curses.A_DIM)
        #
        # await user input
        key = term.getch()
        if key == curses.KEY_RESIZE:
            pass # this deals with resizing the terminal window
        elif key == ord('r'):
            config = configparser.ConfigParser()
            config.read(config_path)
            set_config_data(term, config, config_path)
        elif key == ord('t'):
            config = configparser.ConfigParser()
            config.read(config_path)
            set_config_keybindings(term, config, config_path)
        else:
            break
    #
    term.clear()
    y, x = wrapstr(term, 2, tab, 'connecting to the database, please wait', curses.A_DIM)
    term.refresh() # force update screen
    try: # try to connect to the database (timeout = 10s)
        db = Database(user, host, passwd)
        #
        # setup signal handler (avoids exiting without closing the connection)
        signal.signal(signal.SIGINT, db.signal_handler)
        #
    except Exception as e:
        connection_error_handler(term, e)
    #
    while True:
        term.clear()
        #
        # read db info
        try: # try to query the data
            couplet = db.select_couplets[db.cp_index]
            zero_text, one_text = db.db.show_couplet(couplet)
            species = db.select_species[db.sp_index]
            status = db.db.show_state(species, couplet)
        except Exception as e:
            connection_error_handler(term, e)
        #
        # display db info
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
        y, x = wrapstr(term, y+1, tab, '({}) previous couplet  ({}) next couplet      ({}) update'.format(readkey(PREV_C), readkey(NEXT_C), readkey(UPDATE)), curses.A_DIM)
        y, x = wrapstr(term, y+1, tab, '({}) previous species  ({}) next species      ({}) quit'.format(readkey(PREV_S), readkey(NEXT_S), readkey(QUIT)), curses.A_DIM)
        #
        # await user input
        key = term.getch()
        #
        if key == NEXT_C:
            if db.cp_index < len(db.select_couplets)-1:
                db.cp_index += 1
        elif key == PREV_C:
            if db.cp_index > 0:
                db.cp_index -= 1
        elif key == NEXT_S:
            if db.sp_index < len(db.select_species)-1:
                db.sp_index += 1
        elif key == PREV_S:
            if db.sp_index > 0:
                db.sp_index -= 1
        elif key == UPDATE:
            y, x = wrapstr(term, input_y, tab, 'type a new value to edit the database:')
            curses.curs_set(1)
            curses.echo()
            new_status = term.getstr(y, x+1).decode('utf-8').upper()
            curses.noecho()
            curses.curs_set(0)
            if new_status.upper() == 'NULL_VALUE':
                new_status = None
            elif new_status == '3':
                new_status = 'NA'
            if new_status in ['0', '1', '01', '10', 'NA', None]:
                y, x = wrapstr(term, y+1, tab, 'new status: {}'.format(new_status), curses.A_BOLD)
                y, x = wrapstr(term, y+1, tab, "press '{}' to confirm, or any key to cancel".format(readkey(CONFIRM)))
                confirm = term.getch()
                if confirm == CONFIRM:
                    try: # try to perform an update:
                        db.db.update(species, new_status, couplet)
                        y, x = wrapstr(term, y+1, tab, 'change confirmed, press any key to continue', curses.color_pair(2))
                    except Exception as e:
                        connection_error_handler(term, e)
                else:
                    y, x = wrapstr(term, y+1, tab, 'action cancelled, press any key to continue', curses.color_pair(3))
            else:
                y, x = wrapstr(term, y+1, tab, 'illegal status: {}'.format(new_status), curses.color_pair(3))
                y, x = wrapstr(term, y+1, tab, "please type '0', '1', '01' or 'NA'")
            term.getch()
        elif key == QUIT:
            break
        elif key == curses.KEY_RESIZE:
            pass # this deals with resizing the terminal window
    #
    try: # try to close the connection nicely
        db.db.connection.close()
    except Exception as e:
        connection_error_handler(term, e)


if __name__ == '__main__':
    curses.wrapper(main)
