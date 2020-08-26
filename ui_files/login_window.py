# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(362, 302)
        self.pushButton_changeLoginInfo = QtWidgets.QPushButton(Dialog)
        self.pushButton_changeLoginInfo.setGeometry(QtCore.QRect(30, 230, 141, 41))
        self.pushButton_changeLoginInfo.setObjectName("pushButton_changeLoginInfo")
        self.pushButton_login = QtWidgets.QPushButton(Dialog)
        self.pushButton_login.setGeometry(QtCore.QRect(190, 230, 141, 41))
        self.pushButton_login.setObjectName("pushButton_login")
        self.label_info = QtWidgets.QLabel(Dialog)
        self.label_info.setGeometry(QtCore.QRect(30, 30, 301, 101))
        self.label_info.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_info.setObjectName("label_info")
        self.pushButton_setCoupletFilter = QtWidgets.QPushButton(Dialog)
        self.pushButton_setCoupletFilter.setGeometry(QtCore.QRect(30, 150, 141, 25))
        self.pushButton_setCoupletFilter.setObjectName("pushButton_setCoupletFilter")
        self.pushButton_setSpeciesFilter = QtWidgets.QPushButton(Dialog)
        self.pushButton_setSpeciesFilter.setGeometry(QtCore.QRect(30, 180, 141, 25))
        self.pushButton_setSpeciesFilter.setObjectName("pushButton_setSpeciesFilter")
        self.label_coupletFile = QtWidgets.QLabel(Dialog)
        self.label_coupletFile.setGeometry(QtCore.QRect(190, 150, 141, 21))
        self.label_coupletFile.setObjectName("label_coupletFile")
        self.label_speciesFile = QtWidgets.QLabel(Dialog)
        self.label_speciesFile.setGeometry(QtCore.QRect(190, 180, 141, 21))
        self.label_speciesFile.setObjectName("label_speciesFile")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_changeLoginInfo.setText(_translate("Dialog", "Change Login Info"))
        self.pushButton_login.setText(_translate("Dialog", "Login"))
        self.label_info.setText(_translate("Dialog", "Current Login Info:"))
        self.pushButton_setCoupletFilter.setText(_translate("Dialog", "Set Couplet Filter"))
        self.pushButton_setSpeciesFilter.setText(_translate("Dialog", "Set Species Filter"))
        self.label_coupletFile.setText(_translate("Dialog", "TextLabel"))
        self.label_speciesFile.setText(_translate("Dialog", "TextLabel"))

