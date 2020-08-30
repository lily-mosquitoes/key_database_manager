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
        Dialog.resize(361, 302)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.label_info = QtWidgets.QLabel(Dialog)
        self.label_info.setMinimumSize(QtCore.QSize(270, 120))
        self.label_info.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_info.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_info.setObjectName("label_info")
        self.verticalLayout.addWidget(self.label_info, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_setCoupletFilter = QtWidgets.QPushButton(Dialog)
        self.pushButton_setCoupletFilter.setObjectName("pushButton_setCoupletFilter")
        self.horizontalLayout.addWidget(self.pushButton_setCoupletFilter)
        self.label_coupletFile = QtWidgets.QLabel(Dialog)
        self.label_coupletFile.setObjectName("label_coupletFile")
        self.horizontalLayout.addWidget(self.label_coupletFile)
        spacerItem2 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pushButton_setSpeciesFilter = QtWidgets.QPushButton(Dialog)
        self.pushButton_setSpeciesFilter.setObjectName("pushButton_setSpeciesFilter")
        self.horizontalLayout_2.addWidget(self.pushButton_setSpeciesFilter)
        self.label_speciesFile = QtWidgets.QLabel(Dialog)
        self.label_speciesFile.setObjectName("label_speciesFile")
        self.horizontalLayout_2.addWidget(self.label_speciesFile)
        spacerItem4 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem6 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.pushButton_changeLoginInfo = QtWidgets.QPushButton(Dialog)
        self.pushButton_changeLoginInfo.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_changeLoginInfo.setObjectName("pushButton_changeLoginInfo")
        self.horizontalLayout_3.addWidget(self.pushButton_changeLoginInfo)
        self.pushButton_login = QtWidgets.QPushButton(Dialog)
        self.pushButton_login.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_login.setObjectName("pushButton_login")
        self.horizontalLayout_3.addWidget(self.pushButton_login)
        spacerItem7 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem8 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem8)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_info.setText(_translate("Dialog", "Current Login Info:"))
        self.pushButton_setCoupletFilter.setText(_translate("Dialog", "Set Couplet Filter"))
        self.label_coupletFile.setText(_translate("Dialog", "TextLabel"))
        self.pushButton_setSpeciesFilter.setText(_translate("Dialog", "Set Species Filter"))
        self.label_speciesFile.setText(_translate("Dialog", "TextLabel"))
        self.pushButton_changeLoginInfo.setText(_translate("Dialog", "Change Login Info"))
        self.pushButton_login.setText(_translate("Dialog", "Login"))

