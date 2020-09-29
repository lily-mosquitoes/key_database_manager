import sys
import os
import platform
from urllib.parse import urlparse

import keyring
from keyring.backends import OS_X, Windows
from PyQt5 import QtWidgets

from ui_files import Ui_LoginWindow, Ui_ConfigWindow, Ui_ReportWindow, Ui_MainWindow
from models import ModelDataset
from common_functions import import_bulk_update_file


SERVICE = 'key_database_manager'
USERS_STORAGE = 'users_storage'

# setting up keyring (necessary for Windows and macOS)
system = platform.system()
if system == 'Darwin':
    keyring.set_keyring(OS_X.Keyring())
elif system == 'Windows':
    keyring.set_keyring(Windows.WinVaultKeyring())
else:
    pass # rely on autodiscovery for Linux


class LoginWindow(QtWidgets.QDialog, Ui_LoginWindow):

    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setupUi(self)

        self.UiComponents()

    def UiComponents(self):

        # tool button
        self.menu = QtWidgets.QMenu()
        self.actionAddLogin = QtWidgets.QAction('add login')
        self.actionRemoveLogin = QtWidgets.QAction('remove login')
        for item in [self.actionAddLogin, self.actionRemoveLogin]:
            self.menu.addAction(item)
        self.toolButton.setMenu(self.menu)

        self.showLogins()

        self.showLoginInfo()

        self.comboBox_loginAs.currentIndexChanged.connect(self.showLoginInfo)

        self.pushButton_login.setFocus()

        self.actionAddLogin.triggered.connect(self.addLogin)
        self.actionRemoveLogin.triggered.connect(self.removeLogin)
        self.pushButton_changeLoginInfo.pressed.connect(self.changeLoginInfo)
        self.pushButton_login.pressed.connect(self.db_connect)

    def db_connect(self):

        try:
            self.db = ModelDataset(
                user=self.login_list[self.current_login].username,
                host=self.login_list[self.current_login].hostname, password=self.login_list[self.current_login].password,
                db=self.login_list[self.current_login].path[1:]
            )
        except Exception as e:
            connection_error_handler(e)
        self.hide()

    def _return_users(self):

        users_storage = keyring.get_password(SERVICE, USERS_STORAGE)
        if users_storage:
            users = users_storage.split('|')
            return users
        else:
            raise Exception

    def read_users_storage(self):

        try:
            return self._return_users()

        except Exception:
            config = ConfigWindow()
            config.exec_()
            return self._return_users()

    def read_login_list(self):
        # reading user storage
        try:
            users = self.read_users_storage()
        except Exception:
            self.close()

        # get passwords
        self.login_list = dict()
        for u in users:
            p = keyring.get_password(SERVICE, u)
            u_p = u.replace('@', f':{p}@')
            # each entry is user_name, URL object
            self.login_list[u] = urlparse(f'mysql://{u_p}')

    def showLogins(self):
        # reading login_list
        self.read_login_list()

        # show logins
        self.comboBox_loginAs.addItems(self.login_list.keys())
        self.comboBox_loginAs.repaint() #repaint for MacOS

    def showLoginInfo(self):

        self.current_login = self.comboBox_loginAs.currentText()

        user_text = self.login_list[self.current_login].username
        host_text = self.login_list[self.current_login].hostname
        password_mask = '•'*len(self.login_list[self.current_login].password)
        database_text = self.login_list[self.current_login].path[1:]

        self.label_info.setText(f'Current login info:\n\n    User: {user_text}\n\n    Host: {host_text}\n\n    Password: {password_mask}\n\n    Database: {database_text}')
        self.label_info.repaint() #repaint for MacOS

    def addLogin(self):

        old_login_list = self.login_list.keys()

        config = ConfigWindow()
        config.exec_()

        self.read_login_list()

        # show logins
        item_to_add = set(self.login_list.keys()) - set(old_login_list)
        if len(item_to_add) > 0:
            self.comboBox_loginAs.addItem(item_to_add.pop())
            self.comboBox_loginAs.repaint()
            self.comboBox_loginAs.setCurrentIndex(self.comboBox_loginAs.count()-1)

    def changeLoginInfo(self):

        old_login_list = self.login_list.keys()

        config = ConfigWindow(change=self.current_login)
        config.exec_()

        self.read_login_list()

        # show logins
        item_to_add = set(self.login_list.keys()) - set(old_login_list)
        if len(item_to_add) > 0:
            self.comboBox_loginAs.removeItem(self.comboBox_loginAs.currentIndex())
            self.comboBox_loginAs.addItem(item_to_add.pop())
            self.comboBox_loginAs.repaint()
            self.comboBox_loginAs.setCurrentIndex(self.comboBox_loginAs.count()-1)

    def removeLogin(self):

        login_to_remove = self.comboBox_loginAs.currentText()

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(f'Are you sure you want to delete the login "{login_to_remove}"?')
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        choice = msg.exec_()

        if choice == QtWidgets.QMessageBox.Yes:

            users_storage = keyring.get_password(SERVICE, USERS_STORAGE)
            users = users_storage.split('|')

            # removing user from users_storage
            users.remove(login_to_remove)
            keyring.set_password(SERVICE, USERS_STORAGE, '|'.join(users))
            # removing user from keyring
            keyring.delete_password(SERVICE, login_to_remove)

            self.read_login_list()

            self.comboBox_loginAs.removeItem(self.comboBox_loginAs.currentIndex())
            self.comboBox_loginAs.repaint()

    def closeEvent(self, event):
        sys.exit(0)


class ConfigWindow(QtWidgets.QDialog, Ui_ConfigWindow):

    def __init__(self, change=None):
        super(ConfigWindow, self).__init__()
        self.setupUi(self)

        # get input
        self.change = change
        self.pushButton_setLoginInfo.pressed.connect(self.write_config)

    def write_config(self):

        # accessing users_storage
        users_storage = keyring.get_password(SERVICE, USERS_STORAGE)
        if users_storage:
            users = users_storage.split('|')
        else:
            users = list()

        if self.change:
            # removing user from users_storage
            users.remove(self.change)
            # removing user from keyring
            keyring.delete_password(SERVICE, self.change)

        login_name = f'{self.user.text()}@{self.host.text()}/{self.database.text()}'

        # add user to users_storage
        users.append(login_name)
        keyring.set_password(SERVICE, USERS_STORAGE, '|'.join(users))

        # add user to keyring
        keyring.set_password(SERVICE, login_name, self.password.text())

        self.hide()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # login
        login = LoginWindow()
        login.exec_()

        # current login
        self.current_login = login.current_login

        # database connection
        self.db = login.db

        self.UiComponents()

    def closeEvent(self, event):
        try:
            self.db.connection.close()
        except Exception as e:
            connection_error_handler(e)
        event.accept()

    def UiComponents(self):

        # ui setup
        self.comboBox_couplet.addItems(self.db.db_couplets)
        self.comboBox_species.addItems(self.db.db_species)
        self.comboBox_status.addItems(['0', '1', '01', 'NA'])

        self.onChoose()

        # choose
        self.comboBox_couplet.currentIndexChanged.connect(self.onChoose)
        self.comboBox_species.currentIndexChanged.connect(self.onChoose)

        # couplet next / previous
        self.pushButton_nextCouplet.pressed.connect(lambda: self.onCouplet(1))
        self.pushButton_previousCouplet.pressed.connect(lambda: self.onCouplet(-1))

        # species next / previous
        self.pushButton_nextSpecies.pressed.connect(lambda: self.onSpecies(1))
        self.pushButton_previousSpecies.pressed.connect(lambda: self.onSpecies(-1))

        # update
        self.pushButton_change.pressed.connect(self.onChange)

        # change password action
        self.action_change_my_password.triggered.connect(self.onChangeMyPassword)

        # bulk update action
        self.action_bulk_update.triggered.connect(self.onBulkUpdate)

    def get_new_password(self, message):

        text, okPressed = QtWidgets.QInputDialog.getText(self, message,"New password:", QtWidgets.QLineEdit.Password, "")

        if not okPressed:
            pass
        elif okPressed and len(text) >= 8:
            return text
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Password must be at least 8 characters long.')
            msg.exec_()

    def change_current_user_password(self, text):

        try:
            # change password for current user
            self.db.change_my_password(text)
            keyring.set_password(SERVICE, self.current_login, text)
        except Exception as e:
            connection_error_handler(e)

    def onChoose(self):
        self.c_couplet = str(self.comboBox_couplet.currentText())
        self.c_species = str(self.comboBox_species.currentText())
        #
        try:
            zero_text, one_text = self.db.show_couplet(self.c_couplet)
            state = self.db.show_state(self.c_species, self.c_couplet)
        except Exception as e:
            connection_error_handler(e)
        #
        self.label_couplet.setText('Current couplet: {}'.format(self.c_couplet))
        self.label_couplet.repaint() #repaint for MacOS
        self.label_zero.setText(zero_text)
        self.label_zero.repaint() #repaint for MacOS
        self.label_one.setText(one_text)
        self.label_one.repaint() #repaint for MacOS
        self.label_species.setText(self.c_species)
        self.label_species.repaint() #repaint for MacOS
        self.label_status.setText('Current status: {}'.format(state or 'NULL'))
        self.label_status.repaint() #repaint for MacOS

    def onCouplet(self, add):
        c_couplet_index = self.db.db_couplets.index(self.c_couplet)
        n_couplet_index = c_couplet_index + add
        if n_couplet_index >= len(self.db.db_couplets) or n_couplet_index < 0:
            pass # avoid index out of range
        else:
            self.comboBox_couplet.setCurrentIndex(n_couplet_index)
            self.comboBox_couplet.repaint() #repaint for MacOS
            self.onChoose()

    def onSpecies(self, add):
        c_species_index = self.db.db_species.index(self.c_species)
        n_species_index = c_species_index + add
        if n_species_index >= len(self.db.db_species) or n_species_index < 0:
            pass # avoid index out of range
        else:
            self.comboBox_species.setCurrentIndex(n_species_index)
            self.comboBox_species.repaint() #repaint for MacOS
            self.onChoose()

    def onChange(self):
        try:
            # UPDATE db
            new_state = str(self.comboBox_status.currentText())
            self.db.update(self.c_species, new_state, self.c_couplet)
            # confirm UPDATE
            state = self.db.show_state(self.c_species, self.c_couplet)
            self.label_status.setText('Current status: {}'.format(state or 'NULL'))
            self.label_status.repaint() #repaint for MacOS
        except Exception as e:
            connection_error_handler(e)

    def onChangeMyPassword(self):
        text = self.get_new_password("Type a new password")
        #
        if text == None:
            pass
        else:
            text2 = self.get_new_password("Please type again")
            #
            if text == text2:
                self.change_current_user_password(text)
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Passwords don't match!")
                msg.exec_()

    def onBulkUpdate(self):
        # get path
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open CSV file for bulk update', '', 'CSV files (*.csv)', options=QtWidgets.QFileDialog.DontUseNativeDialog) # not using the native dialog to avoid a Gtk error message related to a Qt bug if I understood it correctly
        if os.path.exists(path) and path.endswith('.csv'):
            rw = ReportWindow(path, self.db)
            rw.exec_()
        else:
            pass


class ReportWindow(QtWidgets.QDialog, Ui_ReportWindow):
    def __init__(self, path, db):
        super(ReportWindow, self).__init__()
        self.setupUi(self)

        # set no close
        self._want_to_close = False

        # database
        self.db = db

        # variables for report
        self.report = {
            'couplets_updated': set(),
            'species_updated': set(),
            'total_states_updated': 0,
            'total_states_not_updated': 0,
        }
        self.couplets, self.species, self.states = import_bulk_update_file(path, self.db.db_couplets, self.db.db_species)

        self.update_list = list()
        for cp in self.couplets:
            for sp in self.species:
                d = {
                    'couplet': {
                        'name': cp,
                        'index': self.couplets.index(cp),
                    },
                    'species': {
                        'name': sp,
                        'index': self.species.index(sp),
                    },
                }
                self.update_list.append(d)

        self.input_flag = False
        self.end_flag = False
        self.error_flag = False

        # display message
        self.message = ''

        self.begin()

    def begin(self):
        while self.end_flag == False:
            self.mainLoop()

        # end
        self.label_report.setText(self.message)
        self.pushButton_ok.setEnabled(True)
        self._want_to_close = True
        self.pushButton_ok.pressed.connect(self.close)

    # overwrite closeEvent to exit on manual close,
    # but proceed normally on button press (sets _want_to_close)
    def closeEvent(self, evnt):
        if self._want_to_close:
            # use closeEvent from parent class
            super(ReportWindow, self).closeEvent(evnt)
        else:
            # ignore close event
            evnt.ignore()

    def mainLoop(self):

        confirmed = self.get_current_pair()
        self.label_report.setText(self.message)
        self.label_report.repaint()
        self.onUpdate(confirmed)

    def get_current_pair(self):

        if len(self.update_list) > 0:

            self.update_pair = self.update_list.pop(0)

            # get state value on csv
            self.update_value = self.states[self.update_pair['couplet']['index']][self.update_pair['species']['index']]

            # get current state on database
            db_value = self.db.show_state(species=self.update_pair['species']['name'], couplet=self.update_pair['couplet']['name'])

            # message
            self.message = "updating couplets... {}/{}\nupdating species... {}/{}".format(self.update_pair['couplet']['index']+1, len(self.couplets), self.update_pair['species']['index']+1, len(self.species))

            if self.update_value == db_value:

                return False # confirm update == False

            elif db_value == None:

                return True # confirm update == True

            elif self.update_value != db_value and db_value != None:

                message = """
                    are you sure you want to change this value?

                        couplet: {}

                        species: {}

                        from {} to {}

                    press 'Yes' to confirm, or 'No' to skip
                """.format(self.update_pair['couplet']['name'], self.update_pair['species']['name'], db_value, self.update_value)

                dlg = ConfirmUpdate(self.message+'\n\n'+message)
                result = dlg.exec_()
                if result:
                    return True # confirm update == True

                else:
                    return False # confirm update == False

        else:
            # print report
            self.message = 'Bulk update finished\n'
            self.message += self.print_report()
            self.end_flag = True
            return None

    def print_report(self):
        # make report string
        message = ''
        for k, v in self.report.items():
            if type(v) == set:
                v = len(v)
            message += "    {}: {}\n".format(k, str(v))
        return message

    def display_error(self, e):
        # print report
        message = self.print_report()
        message += "AN ERROR OCCURED"
        self.label_report.setText(message)
        self.pushButton_ok.setEnabled(True)
        self.pushButton_ok.pressed.connect(lambda: connection_error_handler(e))

    def onUpdate(self, confirmed):

        if confirmed == True:
            try:
                self.db.update(species=self.update_pair['species']['name'], value=self.update_value, couplet=self.update_pair['couplet']['name'])
                self.report['couplets_updated'].add(self.update_pair['couplet']['name'])
                self.report['species_updated'].add(self.update_pair['species']['name'])
                self.report['total_states_updated'] += 1
            except Exception as e:
                self.display_error(e)

        elif confirmed == False:
            self.report['total_states_not_updated'] += 1

        elif confirmed == None:
            pass


class ConfirmUpdate(QtWidgets.QDialog):

    def __init__(self, message):
        super(ConfirmUpdate, self).__init__()

        self.setWindowTitle("Confirm update")

        QBtn = QtWidgets.QDialogButtonBox.Yes | QtWidgets.QDialogButtonBox.No

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.labelMessage = QtWidgets.QLabel()
        self.labelMessage.setText(message)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.labelMessage)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


###
def connection_error_handler(e):
    error_dialog = QtWidgets.QMessageBox()
    error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
    error_dialog.setText('the following error occured:\n\nerr code: {}\nerr msg.: {}\n\nif you feel this is a mistake, contact your database admin'.format(e.args[0], e.args[1]))
    sys.exit(error_dialog.exec_())

def main():
    app = QtWidgets.QApplication([])
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
