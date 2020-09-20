import curses
import signal
import sys
import os
import configparser

from models.model_dataset import ModelDataset
from ta_functions import wrapstr, get_text, readkey, get_file, set_login_config, read_login_config, remove_login_config, set_filter_config, read_filter_config


class Signal(object):
    def __init__(self, db):

        self.db = db

    def signal_handler(self, sig, frame):
        self.db.connection.close()
        sys.exit(0)


def change_current_user_password(term, db, config_path, login_name):

    tab = 8

    # type once
    message = 'Passwords must be at least 8 characters long'
    field = 'please type a new password:'
    text = get_text(term, 2, tab, message, field, password=True)

    # type twice
    message = 'Passwords must be at least 8 characters long'
    field = 'please type again:'
    text2 = get_text(term, 2, tab, message, field, password=True)

    #
    term.clear()

    # check if they are the same and above 8 characters
    if text == text2 and len(text) >= 8:

        try:
            db.change_my_password(text)
            config = configparser.ConfigParser()
            config.read(config_path)
            config.set(login_name, 'password', text)

            with open(config_path, 'w') as configfile:
                config.write(configfile)

            y, x = wrapstr(term, 2, tab, "password changed!", curses.color_pair(2))

        except Exception as e:
            connection_error_handler(term, e)

    elif len(text) < 8:

        y, x = wrapstr(term, 2, tab, "passwords must be at least 8 characters long!", curses.color_pair(3))

    elif text != text2:

        y, x = wrapstr(term, 2, tab, "passwords don't match!", curses.color_pair(3))

    term.getch()

def get_bulk_update_file(term, db):

    path = os.path.abspath(os.path.expanduser('~'))

    choosen_file = get_file(term, path, type='.csv', message='Please choose a .csv file:')

    return choosen_file

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
            db_couplets = db.list_couplets()
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
                db_species = db.list_species()
                if sp not in db_species:
                    report['species_not_found'].add(sp)
                    continue
                else:
                    pass
                # since couplet and species names are unique
                value = states[couplets.index(cp)][species.index(sp)]
                # get current state on database
                db_value = db.show_state(species=sp, couplet=cp)
                if value == db_value:
                    # do nothing
                    report['total_states_not_updated'] += 1
                elif db_value == None:
                    try:
                        db.update(species=sp, value=value, couplet=cp)
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
                                db.update(species=sp, value=value, couplet=cp)
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

def login(term, config_path):

    # highlight
    # curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_MAGENTA)

    # set vars
    tab = 8

    max_lines = 8
    max_cols = 60

    cursor = 0
    line_start = 0

    # write on terminal
    term.clear()

    # message
    message = "Use the up and down arrows to choose your login, press any key to login; press 'c' to change your selected login configuration, press 'n' to create a new login configuration, press 'r' to remove a login entry, press 'f' to set your filter files"
    y, x = wrapstr(term, 2, tab, message, curses.A_BOLD)

    # set subwindows
    rectangle = term.subwin(max_lines+2, max_cols+2, y+2, tab)

    loginswin = rectangle.subwin(max_lines+1, max_cols, y+3, tab+1)

    rectangle_2 = term.subwin(6, max_cols+2, y+max_lines+5, tab)

    infowin = rectangle_2.subwin(5, max_cols, y+max_lines+6, tab+1)

    rectangle_3 = term.subwin(4, max_cols+2, y+(2*max_lines)+4, tab)

    filterwin = rectangle_3.subwin(3, max_cols, y+(2*max_lines)+5, tab+1)

    # confirm configuration
    while True:

        # reading login config dict
        login_config_dict = read_login_config(term, config_path)

        login_list = [l for l in login_config_dict.keys()]

        # reading filter config
        filter_config = read_filter_config(term, config_path)

        # write on terminal
        term.clear()

        # message
        y, x = wrapstr(term, 2, tab, message, curses.A_BOLD)

        loginswin.clear()
        rectangle.border()

        infowin.clear()
        rectangle_2.border()

        filterwin.clear()
        rectangle_3.border()

        y = x = 0
        for login in login_list[line_start:line_start+max_lines]:
            if y == cursor:
                loginswin.addstr(y, x, login, curses.color_pair(2))
            else:
                loginswin.addstr(y, x, login)
            y += 1

        current_login = login_list[line_start:line_start+max_lines][cursor]
        infowin.addstr(0, 0, 'user: {}'.format(login_config_dict[current_login]['user']))
        infowin.addstr(1, 0, 'host: {}'.format(login_config_dict[current_login]['host']))
        infowin.addstr(2, 0, 'password: {}'.format('•'*len(login_config_dict[current_login]['password'])))
        infowin.addstr(3, 0, 'database: {}'.format(login_config_dict[current_login]['database']))

        cp_filter = filter_config['couplets'].split(os.path.sep)[-1]
        sp_filter = filter_config['species'].split(os.path.sep)[-1]
        filterwin.addstr(0, 0, 'couplet filter: {}'.format(cp_filter))
        filterwin.addstr(1, 0, 'couplet filter: {}'.format(sp_filter))

        term.refresh()
        rectangle.refresh()
        loginswin.refresh()
        rectangle_2.refresh()
        infowin.refresh()

        key = term.getch()

        if key == curses.KEY_DOWN:
            if (cursor == max_lines-1 and line_start+max_lines == len(login_list)) or cursor == len(login_list)-1:
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

        elif key == ord('r'):
            y, x = wrapstr(term, 29, tab, "are you sure you want to remove this login? (press 'y' for yes, any other key for no)", curses.color_pair(3))

            confirm = term.getch()

            if confirm == ord('y'):
                current_login = login_list[line_start:line_start+max_lines][cursor]
                remove_login_config(config_path, login_name=current_login)
                cursor = 0
                line_start = 0

        elif key == ord('c'):
            current_login = login_list[line_start:line_start+max_lines][cursor]
            set_login_config(term, config_path, login_name=current_login)
            cursor = 0
            line_start = 0

        elif key == ord('n'):
            set_login_config(term, config_path)
            cursor = 0
            line_start = 0

        elif key == ord('f'):
            set_filter_config(term, config_path)

        elif key == ord('q'):
            sys.exit(0)

        else:
            if filter_config['couplets'] == '' or filter_config['species'] == '':
                y, x = wrapstr(term, 24, tab, 'please set filter files before login!', curses.color_pair(3))

                term.getch()

            else:
                current_login = login_list[line_start:line_start+max_lines][cursor]
                return current_login, login_config_dict[current_login], filter_config

def main(term):

    # define tabspace (x)
    tab = 8

    # hide cursor
    curses.curs_set(0)

    # init color pairs
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    # keybindings
    CHANGE_PASSWORD = ord('P')
    BULK_UPDATE = ord('B')
    NEXT_C = ord('s')
    PREV_C = ord('a')
    NEXT_S = ord('x')
    PREV_S = ord('z')
    UPDATE = ord('\n')
    CONFIRM = ord('\n')
    QUIT = ord('q')

    # config path
    config_path = os.path.join(os.path.dirname(sys.argv[0]), 'config', 'ta_key_data_manager.config')

    # get login vars
    login_name, login_config, filter_config = login(term, config_path)

    # clear terminal
    term.clear()

    y, x = wrapstr(term, 2, tab, 'connecting to the database, please wait', curses.A_DIM)
    term.refresh() # force update screen

    try: # try to connect to the database (timeout = 10s)
        db = ModelDataset(user=login_config['user'], host=login_config['host'], password=login_config['password'], db=login_config['database'])

        sig = Signal(db)

        # setup signal handler (avoids exiting without closing the connection)
        signal.signal(signal.SIGINT, sig.signal_handler)

    except Exception as e:
        connection_error_handler(term, e)

    # open filter files
    cp_filter = open(filter_config['couplets'], 'rt').read().strip().split('\n')
    sp_filter = open(filter_config['species'], 'rt').read().strip().split('\n')

    # set filters
    select_couplets = [c for c in db.list_couplets() if c in cp_filter]
    select_species = [s for s in db.list_species() if s in sp_filter]

    # set internal variables
    sp_index = 0
    cp_index = 0

    # main loop
    while True:

        term.clear()

        # read db info
        try: # try to query the data
            couplet = select_couplets[cp_index]
            zero_text, one_text = db.show_couplet(couplet)
            species = select_species[sp_index]
            status = db.show_state(species, couplet)
        except Exception as e:
            connection_error_handler(term, e)

        # display actions
        y, x = wrapstr(term, 2, tab, 'actions: ({}) change password    ({}) bulk update'.format(readkey(CHANGE_PASSWORD), readkey(BULK_UPDATE)), curses.A_DIM)

        # display db info
        y, x = wrapstr(term, y+2, tab, 'current couplet: {}'.format(couplet))
        y, x = wrapstr(term, y+2, tab+4, '0. {}'.format(zero_text))
        y, x = wrapstr(term, y+2, tab+4, '1. {}'.format(one_text))
        y, x = wrapstr(term, y+2, tab, 'current species: {}'.format(species))
        y, x = wrapstr(term, y+2, tab+4, 'status: {}'.format(status))

        # freeze input y pos
        input_y = y+2

        # display helper text
        y, x = wrapstr(term, y+7, tab, 'keybindings:', curses.A_DIM)
        y, x = wrapstr(term, y+1, tab, '({}) previous couplet  ({}) next couplet      ({}) update'.format(readkey(PREV_C), readkey(NEXT_C), readkey(UPDATE)), curses.A_DIM)
        y, x = wrapstr(term, y+1, tab, '({}) previous species  ({}) next species      ({}) quit'.format(readkey(PREV_S), readkey(NEXT_S), readkey(QUIT)), curses.A_DIM)

        # await user input
        key = term.getch()

        if key == CHANGE_PASSWORD:
            change_current_user_password(term, db, config_path, login_name)

        elif key == BULK_UPDATE:
            bulk_update_file = get_bulk_update_file(term, db)
            if os.path.isfile(bulk_update_file) and bulk_update_file.endswith('.csv'):
                bulk_update(term, db, bulk_update_file)

        elif key == NEXT_C:
            if cp_index < len(select_couplets)-1:
                cp_index += 1

        elif key == PREV_C:
            if cp_index > 0:
                cp_index -= 1

        elif key == NEXT_S:
            if sp_index < len(select_species)-1:
                sp_index += 1

        elif key == PREV_S:
            if sp_index > 0:
                sp_index -= 1

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
                        db.update(species, new_status, couplet)
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

    try: # try to close the connection nicely
        db.connection.close()
    except Exception as e:
        connection_error_handler(term, e)

##
if __name__ == '__main__':
    curses.wrapper(main)
