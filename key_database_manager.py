import sys
import os
import configparser
from PyQt5 import QtWidgets, uic, QtGui
from ui_files.login_window import Ui_Dialog as Ui_LoginWindow
from ui_files.config_window import Ui_Dialog as Ui_ConfigWindow
from ui_files.main_window import Ui_MainWindow
from models.model_dataset import ModelDataset


class LoginWindow(QtWidgets.QDialog, Ui_LoginWindow):
    def __init__(self, config_path, *args, obj=None, **kwargs):
        super(LoginWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        #
        self.config_path = config_path
        # read config file
        try:
            self.user, self.host, self.passwd, self.couplet_filter, self.species_filter = self.read_config()
        except Exception:
            config = ConfigWindow(self.config_path)
            config.exec_()
            self.user, self.host, self.passwd, self.couplet_filter, self.species_filter = self.read_config()
        #
        self.UiComponents()

    def UiComponents(self):
        #
        self.label_info.setText('Current login info:\n\n    User: {}\n\n    Host: {}\n\n'.format(self.user, self.host))
        self.label_info.repaint() #repaint for MacOS
        #
        self.label_coupletFile.setText(self.couplet_filter.split(os.path.sep)[-1])
        self.label_coupletFile.repaint() #repaint for MacOS
        #
        self.label_speciesFile.setText(self.species_filter.split(os.path.sep)[-1])
        self.label_speciesFile.repaint() #repaint for MacOS
        #
        #
        self.pushButton_login.setFocus()
        #
        self.pushButton_setCoupletFilter.pressed.connect(self.setCoupletFilter)
        self.pushButton_setSpeciesFilter.pressed.connect(self.setSpeciesFilter)
        #
        self.pushButton_changeLoginInfo.pressed.connect(self.changeLoginInfo)
        self.pushButton_login.pressed.connect(self.db_connect)

    def db_connect(self):
        try:
            self.db = ModelDataset(user=self.user, host=self.host, password=self.passwd, db='key_database')
        except Exception as e:
            connection_error_handler(e)
        self.hide()

    def changeLoginInfo(self):
        config = ConfigWindow(self.config_path)
        config.exec_()
        self.user, self.host, self.passwd, self.couplet_filter, self.species_filter = self.read_config()
        self.UiComponents()

    def setCoupletFilter(self):
        couplet_filter, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open couplets file', '', 'Text files (*.txt)', options=QtWidgets.QFileDialog.DontUseNativeDialog) # not using the native dialog to avoid a Gtk error message related to a Qt bug if I understood it correctly
        config = configparser.ConfigParser()
        config.read(self.config_path)
        config.set('filter files', 'Couplets', couplet_filter)
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)
        self.label_coupletFile.setText(couplet_filter.split(os.path.sep)[-1])
        self.label_coupletFile.repaint() #repaint for MacOS

    def setSpeciesFilter(self):
        species_filter, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open species file', '', 'Text files (*.txt)', options=QtWidgets.QFileDialog.DontUseNativeDialog) # not using the native dialog to avoid a Gtk error message related to a Qt bug if I understood it correctly
        config = configparser.ConfigParser()
        config.read(self.config_path)
        config.set('filter files', 'Species', species_filter)
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)
        self.label_speciesFile.setText(species_filter.split(os.path.sep)[-1])
        self.label_speciesFile.repaint() #repaint for MacOS

    def read_config(self):
        config = configparser.ConfigParser()
        try:
            config.read(self.config_path)
            user = config.get('mosquito database', 'User')
            host = config.get('mosquito database', 'Host')
            passwd = config.get('mosquito database', 'Password')
            #
            couplet_filter = config.get('filter files', 'Couplets')
            species_filter = config.get('filter files', 'Species')
        except Exception:
            raise Exception('config file not correctly set up')
        #
        return user, host, passwd, couplet_filter, species_filter

    def closeEvent(self, event):
        sys.exit(0)


class ConfigWindow(QtWidgets.QDialog, Ui_ConfigWindow):
    def __init__(self, config_path, *args, obj=None, **kwargs):
        super(ConfigWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        #
        # get input
        self.config_path = config_path
        self.pushButton_setLoginInfo.pressed.connect(self.write_congfig)

    def write_congfig(self):
        # set up config file
        config = configparser.ConfigParser()
        config['mosquito database'] = {
            'User': self.user.text(),
            'Host': self.host.text(),
            'Password': self.password.text()
        }
        if 'filter files' in config:
            pass
        else:
            config['filter files'] = {
                'Couplets': os.path.join(os.path.dirname(sys.argv[0]), 'select', 'COUPLETS.txt'),
                'Species': os.path.join(os.path.dirname(sys.argv[0]), 'select', 'SPECIES.txt'),
            }
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)
        #
        self.hide()

    def closeEvent(self, event):
        if os.path.exists(self.config_path):
            event.accept()
        else:
            sys.exit(0)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
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

    def fetch_select_couplets(self, config):
        file = open(config.get('filter files', 'Couplets')).read().strip().split('\n')
        select_couplets = [c for c in self.db_couplets if c in file]
        return select_couplets

    def fetch_select_species(self, config):
        file = open(config.get('filter files', 'Species')).read().strip().split('\n')
        select_species = [s for s in self.db_species if s in file]
        return select_species

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


###
def connection_error_handler(e):
    error_dialog = QtWidgets.QMessageBox()
    error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
    error_dialog.setText('connection failed with following error:\n\nerr code: {}\nerr msg.: {}\n\ncontact your database admin'.format(e.args[0], e.args[1]))
    sys.exit(error_dialog.exec_())

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
