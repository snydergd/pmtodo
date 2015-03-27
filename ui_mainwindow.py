# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Fri Mar 27 08:15:25 2015
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(464, 345)
        self.verticalLayout_2 = QtGui.QVBoxLayout(MainWindow)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.addButton = QtGui.QPushButton(MainWindow)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.horizontalLayout.addWidget(self.addButton)
        self.completeButton = QtGui.QPushButton(MainWindow)
        self.completeButton.setObjectName(_fromUtf8("completeButton"))
        self.horizontalLayout.addWidget(self.completeButton)
        self.modifyButton = QtGui.QPushButton(MainWindow)
        self.modifyButton.setObjectName(_fromUtf8("modifyButton"))
        self.horizontalLayout.addWidget(self.modifyButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.taskList = QtGui.QListView(MainWindow)
        self.taskList.setObjectName(_fromUtf8("taskList"))
        self.verticalLayout_2.addWidget(self.taskList)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Todo List", None))
        self.addButton.setText(_translate("MainWindow", "Add", None))
        self.completeButton.setText(_translate("MainWindow", "Complete", None))
        self.modifyButton.setText(_translate("MainWindow", "Modify", None))

