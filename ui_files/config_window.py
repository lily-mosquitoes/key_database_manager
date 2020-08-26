# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(302, 302)
        self.user = QtWidgets.QLineEdit(Dialog)
        self.user.setGeometry(QtCore.QRect(110, 80, 171, 25))
        self.user.setObjectName("user")
        self.host = QtWidgets.QLineEdit(Dialog)
        self.host.setGeometry(QtCore.QRect(110, 120, 171, 25))
        self.host.setObjectName("host")
        self.password = QtWidgets.QLineEdit(Dialog)
        self.password.setGeometry(QtCore.QRect(110, 160, 171, 25))
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 80, 71, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 120, 71, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 160, 71, 21))
        self.label_3.setObjectName("label_3")
        self.label_message = QtWidgets.QLabel(Dialog)
        self.label_message.setGeometry(QtCore.QRect(40, 20, 221, 41))
        self.label_message.setObjectName("label_message")
        self.pushButton_setLoginInfo = QtWidgets.QPushButton(Dialog)
        self.pushButton_setLoginInfo.setGeometry(QtCore.QRect(60, 220, 181, 51))
        self.pushButton_setLoginInfo.setObjectName("pushButton_setLoginInfo")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "User:"))
        self.label_2.setText(_translate("Dialog", "Host:"))
        self.label_3.setText(_translate("Dialog", "Password:"))
        self.label_message.setText(_translate("Dialog", "TextLabel"))
        self.pushButton_setLoginInfo.setText(_translate("Dialog", "Set Login Info"))

