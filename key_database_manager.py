import sys
import configparser
from PyQt5 import QtWidgets, uic, QtGui
from ui_files.main_window import Ui_MainWindow
from models.model_dataset import ModelDataset


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, user, host, passwd, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # database connection
        self.db = ModelDataset(user, host, passwd)
        self.db_species = self.db.list_species()
        self.db_couplets = self.db.list_couplets()
        #
        self.select_species = self.fetch_select_species()
        self.select_couplets = self.fetch_select_couplets()
        #
        self.UiComponents()

    def closeEvent(self, event):
        try:
            self.db.connection.close()
        except Exception as e:
            connection_error_handler(e)
        event.accept()

    def UiComponents(self):
        self.comboBox_couplet.addItems(self.select_couplets)
        self.comboBox_species.addItems(self.select_species)
        self.comboBox_status.addItems(['0', '1', '01', 'NA'])
        #
        self.onJumpPress()
        #
        self.pushButton_jump.pressed.connect(self.onJumpPress)
        #
        self.pushButton_nextCouplet.pressed.connect(lambda: self.onCouplet(1))
        self.pushButton_previousCouplet.pressed.connect(lambda: self.onCouplet(-1))
        #
        self.pushButton_nextSpecies.pressed.connect(lambda: self.onSpecies(1))
        self.pushButton_previousSpecies.pressed.connect(lambda: self.onSpecies(-1))
        #
        ### MOST IMPORTTANT BUTTON: UPDATE FUNCTION
        self.pushButton_change.pressed.connect(self.onChange)

    def fetch_select_couplets(self):
        file = open('select/COUPLETS.txt').read().strip().split('\n')
        select_couplets = [c for c in self.db_couplets if c in file]
        return select_couplets

    def fetch_select_species(self):
        file = open('select/SPECIES.txt').read().strip().split('\n')
        select_species = [s for s in self.db_species if s in file]
        return select_species

    def onJumpPress(self):
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
        self.label_zero.setText(zero_text)
        self.label_one.setText(one_text)
        self.label_species.setText(self.c_species)
        self.label_status.setText('Current status: {}'.format(state or 'NULL'))

    def onCouplet(self, add):
        c_couplet_index = self.select_couplets.index(self.c_couplet)
        n_couplet_index = c_couplet_index + add
        self.comboBox_couplet.setCurrentIndex(n_couplet_index)
        self.onJumpPress()

    def onSpecies(self, add):
        c_species_index = self.select_species.index(self.c_species)
        n_species_index = c_species_index + add
        self.comboBox_species.setCurrentIndex(n_species_index)
        self.onJumpPress()

    def onChange(self):
        try:
            # UPDATE db
            new_state = str(self.comboBox_status.currentText())
            self.db.update(self.c_species, new_state, self.c_couplet)
            # confirm UPDATE
            state = self.db.show_state(self.c_species, self.c_couplet)
            self.label_status.setText('Current status: {}'.format(state or 'NULL'))
        except Exception as e:
            connection_error_handler(e)


###
def read_conf():
    config = configparser.ConfigParser()
    config.read('conf/conf')
    user = config['mosquito database']['User']
    host = config['mosquito database']['Host']
    passwd = config['mosquito database']['Password']
    return user, host, passwd

def connection_error_handler(e):
    error_dialog = QtWidgets.QMessageBox()
    error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
    error_dialog.setText('connection failed with following error:\n\nerr code: {}\nerr msg.: {}\n\ncontact your database admin'.format(e.args[0], e.args[1]))
    sys.exit(error_dialog.exec_())

def main():
    app = QtWidgets.QApplication(sys.argv)
    #
    user, host, passwd = read_conf()
    #
    try:
        main = MainWindow(user, host, passwd)
        main.show()
    except Exception as e:
        connection_error_handler(e)
    #
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
