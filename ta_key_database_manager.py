import curses
import signal
import sys
import os
import configparser
import textwrap
from models.model_dataset import ModelDataset


class Database(object):
    def __init__(self, **kwargs):
        self.db = ModelDataset(**kwargs)
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

    def change_my_password(self, text):
        self.db.change_my_password(text)

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
    for i in [('ChangePassword', 'P'), ('BulkUpdate', 'B'), ('NextCouplet', 's'), ('PreviousCouplet', 'a'), ('NextSpecies', 'x'), ('PreviousSpecies', 'z'), ('Update', 'ENTER'), ('Confirm', 'ENTER'), ('Quit', 'q')]:
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
            'ChangePassword': int(config.get('keybindings', 'ChangePassword')),
            'BulkUpdate': int(config.get('keybindings', 'BulkUpdate')),
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
            'ChangePassword': int(config.get('keybindings', 'ChangePassword')),
            'BulkUpdate': int(config.get('keybindings', 'BulkUpdate')),
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

def change_current_user_password(term, db, config_path):
    tab = 8
    term.clear()
    # message
    y, x = wrapstr(term, 2, tab, "Passwords must be at least 8 characters long", curses.A_BOLD)
    y, x = wrapstr(term, y+1, tab, "please don't resize this window", curses.A_DIM)
    # type once
    y, x = wrapstr(term, y+2, tab, "please type a new password:")
    curses.curs_set(1)
    text = term.getstr(y, x+1).decode('utf-8')
    curses.curs_set(0)
    # type twice
    y, x = wrapstr(term, y+2, tab, "please type again:")
    curses.curs_set(1)
    text2 = term.getstr(y, x+1).decode('utf-8')
    curses.curs_set(0)
    # check if they are the same and above 8 characters
    if text == text2 and len(text) >= 8:
        try:
            db.change_my_password(text)
            config = configparser.ConfigParser()
            config.read(config_path)
            config.set('mosquito database', 'Password', text)
            with open(config_path, 'w') as configfile:
                config.write(configfile)
            y, x = wrapstr(term, y+2, tab, "password changed!", curses.color_pair(2))
        except Exception as e:
            connection_error_handler(term, e)
    elif len(text) < 8:
        y, x = wrapstr(term, y+2, tab, "passwords must be at least 8 characters long!", curses.color_pair(3))
    elif text != text2:
        y, x = wrapstr(term, y+2, tab, "passwords don't match!", curses.color_pair(3))
    term.getch()

def get_bulk_update_file(term, db):
    tab = 8
    term.clear()
    # message
    y, x = wrapstr(term, 2, tab, "Inform the file path (must be .csv)", curses.A_BOLD)
    y, x = wrapstr(term, y+1, tab, "please don't resize this window", curses.A_DIM)
    # get path
    y, x = wrapstr(term, y+2, tab, "path:")
    curses.echo()
    curses.curs_set(1)
    path = term.getstr(y, x+1).decode('utf-8')
    curses.noecho()
    curses.curs_set(0)
    if os.path.exists(path):
        bulk_update(term, db, path)
    else:
        y, x = wrapstr(term, y+2, tab, "couldn't find path '{}'".format(path))
        y, x = wrapstr(term, y+2, tab, "press any key to exit")
        term.getch()

def import_bulk_update_file(path):
    file = open(path, 'rt').read().strip().split('\n')
    species = file.pop(0).split(',')[1:]
    couplets = list()
    states = list()
    for line in file:
        l = line.split(',')
        cp_name = l.pop(0)
        couplets.append(cp_name)
        states.append(l.copy())
    return couplets, species, states

def bulk_update(term, db, path):
    # variables for report
    report = {
        'couplets_updated': set(),
        'species_updated': set(),
        'couplets_not_found': set(),
        'species_not_found': set(),
        'total_states_updated': 0,
        'total_states_not_updated': 0,
    }
    #
    tab = 8
    while True:
        term.clear()
        couplets, species, states = import_bulk_update_file(path)
        for cp in couplets:
            # progress message
            term.clear()
            y, x = wrapstr(term, 2, tab, "updating couplets... {}/{}".format(str(couplets.index(cp)), str(len(couplets))), curses.A_BOLD)
            # input validation
            db_couplets = db.db.list_couplets()
            if cp not in db_couplets:
                report['couplets_not_found'].add(cp)
                continue
            else:
                pass
            for sp in species:
                # progress message
                term.clear()
                y, x = wrapstr(term, 2, tab, "updating couplets... {}/{}".format(str(couplets.index(cp)), str(len(couplets))), curses.A_BOLD)
                y, x = wrapstr(term, y+2, tab, "updating species... {}/{}".format(str(species.index(sp)), str(len(species))), curses.A_BOLD)
                # input validation
                db_species = db.db.list_species()
                if sp not in db_species:
                    report['species_not_found'].add(sp)
                    continue
                else:
                    pass
                # since couplet and species names are unique
                value = states[couplets.index(cp)][species.index(sp)]
                # get current state on database
                db_value = db.db.show_state(species=sp, couplet=cp)
                if value == db_value:
                    # do nothing
                    report['total_states_not_updated'] += 1
                elif db_value == None:
                    try:
                        db.db.update(species=sp, value=value, couplet=cp)
                        report['couplets_updated'].add(cp)
                        report['species_updated'].add(sp)
                        report['total_states_updated'] += 1
                    except pymysql.Error as e:
                        # print report
                        term.clear()
                        y = 1
                        for k, v in report.items():
                            if type(v) == set:
                                v = len(v)
                            y, x = wrapstr(term, y+2, tab+4, "{}: {}".format(k, srt(v)))
                        y, x = wrapstr(term, y+2, tab, "AN ERROR OCCURED", curses.A_BOLD | curses.color_pair(3))
                        y, x = wrapstr(term, y+2, tab, "press any key to exit", curses.color_pair(3))
                        while True:
                            key = term.getch()
                            if key == curses.KEY_RESIZE:
                                continue # this deals with resizing the terminal window
                            else:
                                connection_error_handler(term, e)
                elif value != db_value and db_value != None:
                    while True:
                        y += 1
                        y, x = wrapstr(term, y+1, tab, "are you sure you want to change this value?", curses.A_BOLD | curses.color_pair(3))
                        y, x = wrapstr(term, y+2, tab+4, "couplet: {}".format(cp))
                        y, x = wrapstr(term, y+2, tab+4, "species: {}".format(sp))
                        y, x = wrapstr(term, y+2, tab+8, "from {} to {}".format(db_value, value))
                        y, x = wrapstr(term, y+2, tab, "press 'y' to confirm, or any key to skip")
                        key = term.getch()
                        if key == ord('y'):
                            try:
                                db.db.update(species=sp, value=value, couplet=cp)
                                report['couplets_updated'].add(cp)
                                report['species_updated'].add(sp)
                                report['total_states_updated'] += 1
                                y, x = wrapstr(term, y+2, tab, "updated!", curses.color_pair(2))
                                break
                            except pymysql.Error as e:
                                # print report
                                term.clear()
                                y = 1
                                for k, v in report.items():
                                    if type(v) == set :
                                        v = len(v)
                                    y, x = wrapstr(term, y+2, tab+4, "{}: {}".format(k, srt(v)))
                                y, x = wrapstr(term, y+2, tab, "AN ERROR OCCURED", curses.A_BOLD | curses.color_pair(3))
                                y, x = wrapstr(term, y+2, tab, "press any key to exit", curses.color_pair(3))
                                while True:
                                    key = term.getch()
                                    if key == curses.KEY_RESIZE:
                                        continue # this deals with resizing the terminal window
                                    else:
                                        connection_error_handler(term, e)
                        elif key == curses.KEY_RESIZE:
                            continue # this deals with resizing the terminal window
                        else:
                            # skipped
                            report['total_states_not_updated'] += 1
                            break
        # print report
        term.clear()
        y, x = wrapstr(term, 2, tab, "Bulk update finished", curses.A_BOLD | curses.color_pair(2))
        y += 1
        for k, v in report.items():
            if type(v) == set :
                v = len(v)
            y, x = wrapstr(term, y+1, tab+4, "{}: {}".format(k, str(v)))
        y, x = wrapstr(term, y+2, tab, "press any key to exit", curses.color_pair(2))
        while True:
            key = term.getch()
            if key == curses.KEY_RESIZE:
                continue # this deals with resizing the terminal window
            else:
                break
        break

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
        CHANGE_PASSWORD = keybindings['ChangePassword']
        BULK_UPDATE = keybindings['BulkUpdate']
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
        db = Database(user=user, host=host, passwd=passwd, db='key_database')
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
        # display actions
        y, x = wrapstr(term, 2, tab, 'actions: ({}) change password    ({}) bulk update'.format(readkey(CHANGE_PASSWORD), readkey(BULK_UPDATE)), curses.A_DIM)
        #
        # display db info
        y, x = wrapstr(term, y+2, tab, 'current couplet: {}'.format(couplet))
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
        if key == CHANGE_PASSWORD:
            change_current_user_password(term, db, config_path)
        elif key == BULK_UPDATE:
            get_bulk_update_file(term, db)
        elif key == NEXT_C:
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
