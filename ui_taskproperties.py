# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'taskProperties.ui'
#
# Created: Fri Mar 27 14:28:46 2015
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

class Ui_TaskProperties(object):
    def setupUi(self, TaskProperties):
        TaskProperties.setObjectName(_fromUtf8("TaskProperties"))
        TaskProperties.resize(520, 394)
        self.verticalLayout = QtGui.QVBoxLayout(TaskProperties)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.nameLabel = QtGui.QLabel(TaskProperties)
        self.nameLabel.setObjectName(_fromUtf8("nameLabel"))
        self.horizontalLayout.addWidget(self.nameLabel)
        self.nameEntry = QtGui.QLineEdit(TaskProperties)
        self.nameEntry.setObjectName(_fromUtf8("nameEntry"))
        self.horizontalLayout.addWidget(self.nameEntry)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_2 = QtGui.QLabel(TaskProperties)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.schedLiset = QtGui.QListView(TaskProperties)
        self.schedLiset.setObjectName(_fromUtf8("schedLiset"))
        self.verticalLayout.addWidget(self.schedLiset)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.schedAddButton = QtGui.QPushButton(TaskProperties)
        self.schedAddButton.setObjectName(_fromUtf8("schedAddButton"))
        self.horizontalLayout_2.addWidget(self.schedAddButton)
        self.schedDelButton = QtGui.QPushButton(TaskProperties)
        self.schedDelButton.setObjectName(_fromUtf8("schedDelButton"))
        self.horizontalLayout_2.addWidget(self.schedDelButton)
        self.schedModButton = QtGui.QPushButton(TaskProperties)
        self.schedModButton.setObjectName(_fromUtf8("schedModButton"))
        self.horizontalLayout_2.addWidget(self.schedModButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_3 = QtGui.QLabel(TaskProperties)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.statList = QtGui.QListView(TaskProperties)
        self.statList.setObjectName(_fromUtf8("statList"))
        self.verticalLayout.addWidget(self.statList)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.statAddButton = QtGui.QPushButton(TaskProperties)
        self.statAddButton.setObjectName(_fromUtf8("statAddButton"))
        self.horizontalLayout_3.addWidget(self.statAddButton)
        self.statDelButton = QtGui.QPushButton(TaskProperties)
        self.statDelButton.setObjectName(_fromUtf8("statDelButton"))
        self.horizontalLayout_3.addWidget(self.statDelButton)
        self.statModButton = QtGui.QPushButton(TaskProperties)
        self.statModButton.setObjectName(_fromUtf8("statModButton"))
        self.horizontalLayout_3.addWidget(self.statModButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.saveButton = QtGui.QPushButton(TaskProperties)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout_4.addWidget(self.saveButton)
        self.discardButton = QtGui.QPushButton(TaskProperties)
        self.discardButton.setObjectName(_fromUtf8("discardButton"))
        self.horizontalLayout_4.addWidget(self.discardButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(TaskProperties)
        QtCore.QMetaObject.connectSlotsByName(TaskProperties)

    def retranslateUi(self, TaskProperties):
        TaskProperties.setWindowTitle(_translate("TaskProperties", "Task Properties", None))
        self.nameLabel.setText(_translate("TaskProperties", "Job Name", None))
        self.label_2.setText(_translate("TaskProperties", "Schedules", None))
        self.schedAddButton.setText(_translate("TaskProperties", "Add", None))
        self.schedDelButton.setText(_translate("TaskProperties", "Delete", None))
        self.schedModButton.setText(_translate("TaskProperties", "Modify", None))
        self.label_3.setText(_translate("TaskProperties", "Statuses", None))
        self.statAddButton.setText(_translate("TaskProperties", "Add", None))
        self.statDelButton.setText(_translate("TaskProperties", "Delete", None))
        self.statModButton.setText(_translate("TaskProperties", "Modify", None))
        self.saveButton.setText(_translate("TaskProperties", "Save", None))
        self.discardButton.setText(_translate("TaskProperties", "Discard", None))

