# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(901, 690)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)
        self.label_couplet = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_couplet.setFont(font)
        self.label_couplet.setObjectName("label_couplet")
        self.verticalLayout_2.addWidget(self.label_couplet)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.label_zero = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_zero.sizePolicy().hasHeightForWidth())
        self.label_zero.setSizePolicy(sizePolicy)
        self.label_zero.setMinimumSize(QtCore.QSize(300, 180))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_zero.setFont(font)
        self.label_zero.setWordWrap(True)
        self.label_zero.setObjectName("label_zero")
        self.horizontalLayout_3.addWidget(self.label_zero)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.label_one = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_one.sizePolicy().hasHeightForWidth())
        self.label_one.setSizePolicy(sizePolicy)
        self.label_one.setMinimumSize(QtCore.QSize(300, 180))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_one.setFont(font)
        self.label_one.setWordWrap(True)
        self.label_one.setObjectName("label_one")
        self.horizontalLayout_2.addWidget(self.label_one)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.label_species = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_species.setFont(font)
        self.label_species.setObjectName("label_species")
        self.verticalLayout_2.addWidget(self.label_species)
        self.label_status = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_status.setFont(font)
        self.label_status.setObjectName("label_status")
        self.verticalLayout_2.addWidget(self.label_status)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6, 0, QtCore.Qt.AlignLeft)
        self.comboBox_status = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_status.sizePolicy().hasHeightForWidth())
        self.comboBox_status.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.comboBox_status.setFont(font)
        self.comboBox_status.setObjectName("comboBox_status")
        self.horizontalLayout_4.addWidget(self.comboBox_status, 0, QtCore.Qt.AlignLeft)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.pushButton_change = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_change.sizePolicy().hasHeightForWidth())
        self.pushButton_change.setSizePolicy(sizePolicy)
        self.pushButton_change.setMinimumSize(QtCore.QSize(220, 80))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pushButton_change.setFont(font)
        self.pushButton_change.setObjectName("pushButton_change")
        self.verticalLayout_2.addWidget(self.pushButton_change, 0, QtCore.Qt.AlignLeft)
        spacerItem3 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem5)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.comboBox_couplet = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_couplet.sizePolicy().hasHeightForWidth())
        self.comboBox_couplet.setSizePolicy(sizePolicy)
        self.comboBox_couplet.setMinimumSize(QtCore.QSize(300, 0))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.comboBox_couplet.setFont(font)
        self.comboBox_couplet.setObjectName("comboBox_couplet")
        self.verticalLayout_3.addWidget(self.comboBox_couplet)
        spacerItem6 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem6)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.comboBox_species = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_species.setMinimumSize(QtCore.QSize(300, 0))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.comboBox_species.setFont(font)
        self.comboBox_species.setObjectName("comboBox_species")
        self.verticalLayout_3.addWidget(self.comboBox_species)
        self.horizontalLayout_7.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        spacerItem7 = QtWidgets.QSpacerItem(20, 200, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton_previousCouplet = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_previousCouplet.sizePolicy().hasHeightForWidth())
        self.pushButton_previousCouplet.setSizePolicy(sizePolicy)
        self.pushButton_previousCouplet.setMinimumSize(QtCore.QSize(140, 100))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pushButton_previousCouplet.setFont(font)
        self.pushButton_previousCouplet.setObjectName("pushButton_previousCouplet")
        self.horizontalLayout_6.addWidget(self.pushButton_previousCouplet)
        self.pushButton_nextCouplet = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_nextCouplet.sizePolicy().hasHeightForWidth())
        self.pushButton_nextCouplet.setSizePolicy(sizePolicy)
        self.pushButton_nextCouplet.setMinimumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pushButton_nextCouplet.setFont(font)
        self.pushButton_nextCouplet.setObjectName("pushButton_nextCouplet")
        self.horizontalLayout_6.addWidget(self.pushButton_nextCouplet)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton_previousSpecies = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_previousSpecies.sizePolicy().hasHeightForWidth())
        self.pushButton_previousSpecies.setSizePolicy(sizePolicy)
        self.pushButton_previousSpecies.setMinimumSize(QtCore.QSize(140, 100))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pushButton_previousSpecies.setFont(font)
        self.pushButton_previousSpecies.setObjectName("pushButton_previousSpecies")
        self.horizontalLayout_5.addWidget(self.pushButton_previousSpecies)
        self.pushButton_nextSpecies = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_nextSpecies.sizePolicy().hasHeightForWidth())
        self.pushButton_nextSpecies.setSizePolicy(sizePolicy)
        self.pushButton_nextSpecies.setMinimumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pushButton_nextSpecies.setFont(font)
        self.pushButton_nextSpecies.setObjectName("pushButton_nextSpecies")
        self.horizontalLayout_5.addWidget(self.pushButton_nextSpecies)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        spacerItem8 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem8)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem9 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem9)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 901, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuChange_Password = QtWidgets.QMenu(self.menuBar)
        self.menuChange_Password.setObjectName("menuChange_Password")
        MainWindow.setMenuBar(self.menuBar)
        self.action_change_my_password = QtWidgets.QAction(MainWindow)
        self.action_change_my_password.setObjectName("action_change_my_password")
        self.action_bulk_update = QtWidgets.QAction(MainWindow)
        self.action_bulk_update.setObjectName("action_bulk_update")
        self.menuChange_Password.addAction(self.action_change_my_password)
        self.menuChange_Password.addAction(self.action_bulk_update)
        self.menuBar.addAction(self.menuChange_Password.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Key Database Manager"))
        self.label_couplet.setText(_translate("MainWindow", "Couplet name: "))
        self.label.setText(_translate("MainWindow", "0. "))
        self.label_zero.setText(_translate("MainWindow", "TextLabel"))
        self.label_2.setText(_translate("MainWindow", "1. "))
        self.label_one.setText(_translate("MainWindow", "TextLabel"))
        self.label_species.setText(_translate("MainWindow", "Species name:"))
        self.label_status.setText(_translate("MainWindow", "Current status: "))
        self.label_6.setText(_translate("MainWindow", "Change status to: "))
        self.pushButton_change.setText(_translate("MainWindow", "Change!"))
        self.label_3.setText(_translate("MainWindow", "Select couplet:"))
        self.label_4.setText(_translate("MainWindow", "Select species:"))
        self.pushButton_previousCouplet.setText(_translate("MainWindow", "Previous couplet"))
        self.pushButton_nextCouplet.setText(_translate("MainWindow", "Next couplet"))
        self.pushButton_previousSpecies.setText(_translate("MainWindow", "Previous species"))
        self.pushButton_nextSpecies.setText(_translate("MainWindow", "Next species"))
        self.menuChange_Password.setTitle(_translate("MainWindow", "Actions"))
        self.action_change_my_password.setText(_translate("MainWindow", "Change my password"))
        self.action_bulk_update.setText(_translate("MainWindow", "Bulk update (from .csv)"))

