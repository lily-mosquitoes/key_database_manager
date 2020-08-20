import curses
import signal
import sys
import configparser
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
    keybindings = {
        'NextCouplet': read_key(config['ta keybindings']['NextCouplet']) or 's',
        'PreviousCouplet': read_key(config['ta keybindings']['PreviousCouplet']) or 'a',
        'NextSpecies': read_key(config['ta keybindings']['NextSpecies']) or 'x',
        'PreviousSpecies': read_key(config['ta keybindings']['PreviousSpecies']) or 'z',
        'Update': read_key(config['ta keybindings']['Update']) or '\n',
        'Cancel': read_key(config['ta keybindings']['Cancel']) or 'c',
        'Quit': read_key(config['ta keybindings']['Quit'] or 'q')
    }

    return user, host, passwd, keybindings

def main(term):
    #
    def signal_handler(sig, frame):
        ## code adapted from: https://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python
        print('You pressed Ctrl+C!')
        db.db.connection.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    #
    term.clear()
    #
    # reading config:
    user, host, passwd, keybindings = read_conf()
    #
    db = Database(user, host, passwd)
    #
    while True:
        term.clear()
        #
        couplet = db.select_couplets[db.cp_index]
        zero_text, one_text = db.db.show_couplet(couplet)
        species = db.select_species[db.sp_index]
        status = db.db.show_state(species, couplet)
        #
        term.addstr("""
        current couplet: {}

            0. {}

            1. {}


        current species: {}

            status: {}

        """.format(couplet, zero_text, one_text, species, status))
        term.refresh()
        y, x = term.getyx()
        #
        key = term.getch()
        #
        if key == keybindings['NextCouplet']:
            if db.cp_index < len(db.select_couplets):
                db.cp_index += 1
        elif key == keybindings['PreviousCouplet']:
            if db.cp_index > 0:
                db.cp_index -= 1
        elif key == keybindings['NextSpecies']:
            if db.sp_index < len(db.select_species):
                db.sp_index += 1
        elif key == keybindings['PreviousSpecies']:
            if db.sp_index > 0:
                db.sp_index -= 1
        elif key == keybindings['Update']:
            term.addstr(y, x, 'type a new value to edit the database: ')
            curses.echo()
            new_status = term.getstr().decode('utf-8').upper()
            curses.noecho()
            if new_status in ['0', '1', '01', '10', 'NA']:
                term.addstr(y+1, x, 'new status: {}'.format(new_status))
                term.addstr(y+2, x, "press any key to confirm, 'c' to cancel")
                confirm = term.getch()
                if confirm == keybindings['Cancel']:
                    term.addstr(y+3, x, 'action cancelled, press any key to continue')
                else:
                    db.db.update(species, new_status, couplet)
                    term.addstr(y+3, x, 'change confirmed, press any key to continue')
            else:
                term.addstr(y+1, x, 'illegal status: {}'.format(new_status))
                term.addstr(y+2, x, "please type '0', '1', '01' or 'NA'")
            term.getch()
        elif key == keybindings['Quit']:
            break

    db.db.connection.close()


if __name__ == '__main__':
    curses.wrapper(main)
