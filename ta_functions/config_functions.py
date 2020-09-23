import os
import configparser
import curses

from . import wrapstr, get_text, get_file


def set_login_config(term, config_path, login_name=None):

    tab = 8

    message = 'please configure your user, host and password'

    login_config = dict()

    for field in ['user', 'host', 'password', 'database']:

        if field == 'password':
            password = True
        else:
            password = False

        value = get_text(term, 2, tab, message, field, password=password)

        login_config[field] = value

    # write login info
    config = configparser.ConfigParser()

    if os.path.exists(config_path):
        config.read(config_path)

    if login_name:
        config.remove_section(login_name)

    login_name = 'login: {}@{}:{}'.format(login_config['user'], login_config['host'], login_config['database'])

    if not config.has_section(login_name):
        config.add_section(login_name)

    for k, v in login_config.items():
        config.set(login_name, k, v)

    with open(config_path, 'w') as configfile:
        config.write(configfile)

def _return_login_config(config_path):

    config = configparser.ConfigParser()

    config.read(config_path)

    sections = config.sections()

    login_config_dict = dict()

    for login in [i for i in sections if 'login: ' in i]:

        login_config = dict()
        for field in ['user', 'host', 'password', 'database']:
            login_config[field] = config.get(login, field)

        login_config_dict[login] = login_config

    return login_config_dict

def read_login_config(term, config_path):

    try:
        return _return_login_config(config_path)

    except Exception:
        set_login_config(term, config_path)
        return _return_login_config(config_path)

def remove_login_config(config_path, login_name):

    config = configparser.ConfigParser()

    config.read(config_path)

    config.remove_section(login_name)

    with open(config_path, 'w') as configfile:
        config.write(configfile)
