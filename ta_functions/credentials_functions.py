import os
import keyring
import curses

from . import wrapstr, get_text, get_file


SERVICE = 'key_database_manager'
USERS_STORAGE = 'users_storage'

def set_login_credential(term, login_name=None):

    tab = 8

    message = 'please configure your user, host and password'

    login_credential = dict()

    for field in ['user', 'host', 'password', 'database']:

        if field == 'password':
            password = True
        else:
            password = False

        value = get_text(term, 2, tab, message, field, password=password)

        login_credential[field] = value

    # accessing users_storage
    users_storage = keyring.get_password(SERVICE, USERS_STORAGE)
    if users_storage:
        users = users_storage.split('|')
    else:
        users = list()

    if login_name:
        # removing user from users_storage
        users.remove(login_name)
        # removing user from keyring
        keyring.delete_password(SERVICE, login_name)

    user_text = login_credential['user']
    host_text = login_credential['host']
    database_text = login_credential['database']
    login_name = f'{user_text}@{host_text}/{database_text}'

    # add user to users_storage
    users.append(login_name)
    keyring.set_password(SERVICE, USERS_STORAGE, '|'.join(users))

    # add user to keyring
    keyring.set_password(SERVICE, login_name, login_credential['password'])

def _return_users():

    users_storage = keyring.get_password(SERVICE, 'users_storage')
    if users_storage:
        users = users_storage.split('|')
        return users
    else:
        raise Exception

def read_users_storage(term):

    try:
        return _return_users()

    except Exception:
        set_login_credential(term)
        return _return_users()

def remove_login_credential(login_name):

    users_storage = keyring.get_password(SERVICE, USERS_STORAGE)
    users = users_storage.split('|')

    # removing user from users_storage
    users.remove(login_name)
    keyring.set_password(SERVICE, USERS_STORAGE, '|'.join(users))
    # removing user from keyring
    keyring.delete_password(SERVICE, login_name)
