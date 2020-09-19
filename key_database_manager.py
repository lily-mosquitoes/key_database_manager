import sys
import os
import configparser
from PyQt5 import QtWidgets
from ui_files.login_window import Ui_Dialog as Ui_LoginWindow
from ui_files.config_window import Ui_Dialog as Ui_ConfigWindow
from ui_files.report_window import Ui_Dialog as Ui_ReportWindow
from ui_files.main_window import Ui_MainWindow
from models.model_dataset import ModelDataset


class LoginWindow(QtWidgets.QDialog, Ui_LoginWindow):
    def __init__(self, config_path):
        super(LoginWindow, self).__init__()
        self.setupUi(self)
        #
        self.config_path = config_path
        # read config file
        try:
            self.login_dict = self.read_login_config()
        except Exception:
            config = ConfigWindow(config_path=self.config_path)
            config.exec_()
            self.login_dict = self.read_login_config()
        #
        self.UiComponents()

    def UiComponents(self):
        #
        self.comboBox_loginAs.addItems(self.login_dict.keys())
        self.comboBox_loginAs.repaint() #repaint for MacOS
        #
        self.onLoginAs()
        #
        self.comboBox_loginAs.currentIndexChanged.connect(self.onLoginAs)
        #
        # read filter config
        self.showFilters()
        #
        self.pushButton_login.setFocus()
        #
        self.pushButton_setCoupletFilter.pressed.connect(self.setCoupletFilter)
        self.pushButton_setSpeciesFilter.pressed.connect(self.setSpeciesFilter)
        #
        self.pushButton_addLogin.pressed.connect(self.addLogin)
        self.pushButton_changeLoginInfo.pressed.connect(self.changeLoginInfo)
        self.pushButton_login.pressed.connect(self.db_connect)

    def db_connect(self):
        # read filters first
        couplet_filter, species_filter = self.read_filter_config()
        if os.path.exists(couplet_filter) and os.path.exists(species_filter):
            try:
                self.db = ModelDataset(user=self.login_dict[self.current_login]['user'], host=self.login_dict[self.current_login]['host'], password=self.login_dict[self.current_login]['password'], db=self.login_dict[self.current_login]['database'])
            except Exception as e:
                connection_error_handler(e)
            self.hide()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Please set valid filters!")
            msg.exec_()

    def showFilters(self):
        #
        couplet_filter, species_filter = self.read_filter_config()
        #
        self.label_coupletFile.setText(couplet_filter.split(os.path.sep)[-1])
        self.label_coupletFile.repaint() #repaint for MacOS
        #
        self.label_speciesFile.setText(species_filter.split(os.path.sep)[-1])
        self.label_speciesFile.repaint() #repaint for MacOS

    def onLoginAs(self):
        #
        self.current_login = self.comboBox_loginAs.currentText()
        #
        self.label_info.setText('Current login info:\n\n    User: {}\n\n    Host: {}\n\n    Password: {}\n\n    Database: {}'.format(self.login_dict[self.current_login]['user'], self.login_dict[self.current_login]['host'], '•'*len(self.login_dict[self.current_login]['password']), self.login_dict[self.current_login]['database']))
        self.label_info.repaint() #repaint for MacOS

    def addLogin(self):
        config = ConfigWindow(config_path=self.config_path)
        config.exec_()
        self.login_dict = self.read_login_config()
        self.comboBox_loginAs.addItem(config.login_text)
        self.comboBox_loginAs.repaint() #repaint for MacOS

    def changeLoginInfo(self):
        config = ConfigWindow(config_path=self.config_path, change='login: {}'.format(self.current_login))
        config.exec_()
        self.login_dict = self.read_login_config()
        self.comboBox_loginAs.setCurrentText(config.login_text)
        self.comboBox_loginAs.repaint() #repaint for MacOS

    def setCoupletFilter(self):
        couplet_filter, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open couplets file', '', 'Text files (*.txt)', options=QtWidgets.QFileDialog.DontUseNativeDialog) # not using the native dialog to avoid a Gtk error message related to a Qt bug if I understood it correctly
        config = configparser.ConfigParser()
        config.read(self.config_path)
        #
        sections = config.sections()
        if 'filter files' not in sections:
            config.add_section('filter files')
        config.set('filter files', 'couplets', couplet_filter)
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)
        self.showFilters()

    def setSpeciesFilter(self):
        species_filter, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open species file', '', 'Text files (*.txt)', options=QtWidgets.QFileDialog.DontUseNativeDialog) # not using the native dialog to avoid a Gtk error message related to a Qt bug if I understood it correctly
        config = configparser.ConfigParser()
        config.read(self.config_path)
        #
        sections = config.sections()
        if 'filter files' not in sections:
            config.add_section('filter files')
        config.set('filter files', 'species', species_filter)
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)
        self.showFilters()

    def read_login_config(self):
        config = configparser.ConfigParser()
        try:
            config.read(self.config_path)
            sections = config.sections()
            if sections == [] or [i for i in sections if 'login: ' in i] == []:
                raise Exception
            else:
                pass
            #
            login_dict = dict()
            for login in [i for i in sections if 'login: ' in i]:
                # this seems useless but it will catch if a user accidentally deletes a line from the config file
                l = {
                    'user': config.get(login, 'user'),
                    'host': config.get(login, 'host'),
                    'password': config.get(login, 'password'),
                    'database': config.get(login, 'database'),
                }
                login_dict[login.strip('login: ')] = l
        except Exception:
            raise Exception('config file not correctly set up')
        #
        return login_dict

    def read_filter_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        try:
            couplet_filter = config.get('filter files', 'couplets')
        except Exception:
            couplet_filter = ''
        try:
            species_filter = config.get('filter files', 'species')
        except Exception:
            species_filter = ''
        #
        return couplet_filter, species_filter

    def closeEvent(self, event):
        sys.exit(0)


class ConfigWindow(QtWidgets.QDialog, Ui_ConfigWindow):
    def __init__(self, config_path, change=None):
        super(ConfigWindow, self).__init__()
        self.setupUi(self)
        #
        # get input
        self.change = change
        self.config_path = config_path
        self.pushButton_setLoginInfo.pressed.connect(self.write_congfig)

    def write_congfig(self):
        config = configparser.ConfigParser()
        #
        if not os.path.exists(self.config_path):
            pass
        else:
            config.read(self.config_path)
        # delete previous entry if given
        if self.change:
            config.remove_section(self.change)
        # set up config file
        self.login_text = 'login: {}@{}:{}'.format(self.user.text(), self.host.text(), self.database.text())
        try:
            config.add_section(self.login_text)
            config.set(self.login_text, 'User', self.user.text())
            config.set(self.login_text, 'Host', self.host.text())
            config.set(self.login_text, 'Password', self.password.text())
            config.set(self.login_text, 'Database', self.database.text())
            #
            with open(self.config_path, 'w') as configfile:
                config.write(configfile)
        #
        except configparser.DuplicateSectionError:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Login already exists!")
            msg.exec_()
        #
        self.hide()

    def closeEvent(self, event):
        if os.path.exists(self.config_path):
            event.accept()
        else:
            sys.exit(0)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        #
        # login
        self.config_path = os.path.join(os.path.dirname(sys.argv[0]), 'config', 'key_data_manager.config')
        login = LoginWindow(self.config_path)
        login.exec_()
        #
        # database connection
        self.db = login.db
        #
        self.UiComponents()

    def closeEvent(self, event):
        try:
            self.db.connection.close()
        except Exception as e:
            connection_error_handler(e)
        event.accept()

    def UiComponents(self):
        #
        # data query
        self.db_species = self.db.list_species()
        self.db_couplets = self.db.list_couplets()
        #
        # filtering
        config = configparser.ConfigParser()
        config.read(self.config_path)
        self.select_species = self.fetch_select_species(config)
        self.select_couplets = self.fetch_select_couplets(config)
        #
        # ui setup
        self.comboBox_couplet.addItems(self.select_couplets)
        self.comboBox_species.addItems(self.select_species)
        self.comboBox_status.addItems(['0', '1', '01', 'NA'])
        #
        self.onChoose()
        #
        self.comboBox_couplet.currentIndexChanged.connect(self.onChoose)
        self.comboBox_species.currentIndexChanged.connect(self.onChoose)
        #
        self.pushButton_nextCouplet.pressed.connect(lambda: self.onCouplet(1))
        self.pushButton_previousCouplet.pressed.connect(lambda: self.onCouplet(-1))
        #
        self.pushButton_nextSpecies.pressed.connect(lambda: self.onSpecies(1))
        self.pushButton_previousSpecies.pressed.connect(lambda: self.onSpecies(-1))
        #
        ### MOST IMPORTANT BUTTON: UPDATE FUNCTION
        self.pushButton_change.pressed.connect(self.onChange)
        #
        # change password action
        self.action_change_my_password.triggered.connect(self.onChangeMyPassword)
        #
        # bulk update action
        self.action_bulk_update.triggered.connect(self.onBulkUpdate)

    def fetch_select_couplets(self, config):
        file = open(config.get('filter files', 'Couplets')).read().strip().split('\n')
        select_couplets = [c for c in self.db_couplets if c in file]
        return select_couplets

    def fetch_select_species(self, config):
        file = open(config.get('filter files', 'Species')).read().strip().split('\n')
        select_species = [s for s in self.db_species if s in file]
        return select_species

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
            config = configparser.ConfigParser()
            config.read(self.config_path)
            config.set('mosquito database', 'Password', text)
            with open(self.config_path, 'w') as configfile:
                config.write(configfile)
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
        c_couplet_index = self.select_couplets.index(self.c_couplet)
        n_couplet_index = c_couplet_index + add
        if n_couplet_index >= len(self.select_couplets) or n_couplet_index < 0:
            pass # avoid index out of range
        else:
            self.comboBox_couplet.setCurrentIndex(n_couplet_index)
            self.comboBox_couplet.repaint() #repaint for MacOS
            self.onChoose()

    def onSpecies(self, add):
        c_species_index = self.select_species.index(self.c_species)
        n_species_index = c_species_index + add
        if n_species_index >= len(self.select_species) or n_species_index < 0:
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
        #
        # set no close
        self._want_to_close = False
        #
        # database
        self.db = db
        #
        # variables for report
        self.report = {
            'couplets_updated': set(),
            'species_updated': set(),
            'couplets_not_found': set(),
            'species_not_found': set(),
            'total_states_updated': 0,
            'total_states_not_updated': 0,
        }
        self.couplets, self.species, self.states = self.import_bulk_update_file(path)
        #
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
        # self.update_list = iter(self.update_list)
        #
        self.input_flag = False
        self.end_flag = False
        self.error_flag = False
        #
        # input validation
        self.db_couplets = self.db.list_couplets()
        self.db_species = self.db.list_species()
        #
        # display message
        self.message = ''
        #
        while self.end_flag == False:
            self.mainLoop()
        #
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
        #
        confirmed = self.get_current_pair()
        self.label_report.setText(self.message)
        self.onUpdate(confirmed)

    def import_bulk_update_file(self, path):
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

    def get_current_pair(self):
        if len(self.update_list) > 0:
            #
            self.update_pair = self.update_list.pop(0)
            #
            if self.update_pair['couplet']['name'] not in self.db_couplets:
                #
                self.report['couplets_not_found'].add(self.update_pair['couplet']['name'])
                #
                self.message = "updating couplets... {}/{}".format(self.update_pair['couplet']['index'], len(self.couplets))
                #
                return None
            #
            elif self.update_pair['species']['name'] not in self.db_species:
                #
                self.report['species_not_found'].add(self.update_pair['species']['name'])
                #
                self.message = "updating couplets... {}/{}\nupdating species... {}/{}".format(self.update_pair['couplet']['index'], len(self.couplets), self.update_pair['species']['index'], len(self.species))
                #
                return None
            else:
                # get state value on csv
                self.update_value = self.states[self.update_pair['couplet']['index']][self.update_pair['species']['index']]
                # get current state on database
                db_value = self.db.show_state(species=self.update_pair['species']['name'], couplet=self.update_pair['couplet']['name'])
                #
                if self.update_value == db_value:
                    #
                    self.message = "updating couplets... {}/{}\nupdating species... {}/{}".format(self.update_pair['couplet']['index'], len(self.couplets), self.update_pair['species']['index'], len(self.species))
                    #
                    return False # confirm update == False
                #
                elif db_value == None:
                    #
                    self.message = "updating couplets... {}/{}\nupdating species... {}/{}".format(self.update_pair['couplet']['index'], len(self.couplets), self.update_pair['species']['index'], len(self.species))
                    #
                    return True # confirm update == True
                #
                elif self.update_value != db_value and db_value != None:
                    message = """
                        are you sure you want to change this value?

                            couplet: {}

                            species: {}

                            from {} to {}

                        press 'Yes' to confirm, or 'No' to skip
                    """.format(self.update_pair['couplet']['name'], self.update_pair['species']['name'], db_value, self.update_value)
                    #
                    dlg = ConfirmUpdate(message)
                    result = dlg.exec_()
                    if result:
                        #
                        self.message = "updating couplets... {}/{}\nupdating species... {}/{}".format(self.update_pair['couplet']['index'], len(self.couplets), self.update_pair['species']['index'], len(self.species))
                        #
                        return True # confirm update == True
                    else:
                        #
                        self.message = "updating couplets... {}/{}\nupdating species... {}/{}".format(self.update_pair['couplet']['index'], len(self.couplets), self.update_pair['species']['index'], len(self.species))
                        #
                        return False # confirm update == False
        #
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
    error_dialog.setText('connection failed with following error:\n\nerr code: {}\nerr msg.: {}\n\ncontact your database admin'.format(e.args[0], e.args[1]))
    sys.exit(error_dialog.exec_())

def main():
    app = QtWidgets.QApplication([])
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
