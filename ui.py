#!/bin/env python

import sys
from PyQt4.QtGui import *
from ui_mainwindow import Ui_MainWindow
from ui_taskproperties import Ui_TaskProperties

class BackendInterface:
    stuff = [{'name': 'hi', 'id': 20}, {'name': 'bob', 'id': 21}, {'name': 'how', 'id': 22}, {'name': 'are', 'id': 23}, {'name': 'you', 'id': 24}]
    @staticmethod
    def taskList():
        return BackendInterface.stuff
    @staticmethod
    def completeTasks(task_ids):
        item_ids = sorted(task_ids, reverse=True)
        for item in item_ids:
            del BackendInterface.stuff[item]
    @staticmethod
    def saveTask(data):
        if not 'id' in data:
            return False
        
        for item in BackendInterface.stuff:
            if item['id'] == data['id']:
                for key, value in data.iteritems():
                    item[key] = value
        return True
    @staticmethod
    def getTask(data):
        # TODO: check for more than just ID, and prepare for if there isn't one
        for item in BackendInterface.stuff:
            if item['id'] == data['id']:
                return item
        return False
            

class MainWindow(QWidget):
    def __init__(self, backendInterface):
        QWidget.__init__(self)

        # class-use attributes
        self.taskModWindow = None
        self.backendInterface = backendInterface
        self.taskModel = None
        self.dataForItem = []

        # Set up the user interface from the designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.refreshTaskList()
        
        # Connect the buttons
        self.ui.addButton.clicked.connect(self.addButtonPushed)
        self.ui.completeButton.clicked.connect(self.completeButtonPushed)
        self.ui.modifyButton.clicked.connect(self.modifyButtonPushed)

    # callbacks
    def addButtonPushed(self, event):
        ok = QMessageBox.information(self, 'Add',
            "Add dialog will be here.", QMessageBox.Ok,
            QMessageBox.Ok)

    def completeButtonPushed(self, event):
        vals = []
        i = 0
        while (self.taskModel.item(i)):
            if self.taskModel.item(i).checkState():
                vals.insert(0,i)
            i += 1
        for i in vals:
            self.taskModel.removeRow(i)
            del self.dataForItem[i]
        self.backendInterface.completeTasks(vals)
    def modifyButtonPushed(self, event):
        task = self.getFirstChecked()
        if task == False:
            # TODO: change just return once out of debug
            task = 0
        i = 0
        checkedTasks = []
        while (self.taskModel.item(i)):
            if self.taskModel.item(i).checkState():
                checkedTasks.append((i,self.taskModel.item(i).checkState()))
            i += 1
        self.taskModWindow = TaskProperties(self.backendInterface, task)
        self.taskModWindow.exec_()
        self.refreshTaskList()
        for task in checkedTasks:
            self.taskModel.item(task[0]).setCheckState(task[1])
    
    # internal functions
    def getFirstChecked(self):
        i = 0
        while (self.taskModel.item(i)):
            if self.taskModel.item(i).checkState():
                return self.dataForItem[i]['id']
            i += 1
        return False
    def refreshTaskList(self):
        tasks = self.backendInterface.taskList()
        model = QStandardItemModel(self.ui.taskList)
        self.dataForItem = []
        for task in tasks:
            name = QStandardItem(task['name'])
            name.setCheckable(True)
            self.dataForItem.append(task)
            model.appendRow(name)
        self.taskModel = model
        self.ui.taskList.setModel(model)

class TaskProperties(QDialog):
    def __init__(self, backendInterface, task):
        QDialog.__init__(self)

        # internal use data
        self.backendInterface = backendInterface
        self.taskId = task
        self.data = backendInterface.getTask({'id': task})

        # initialize UI
        self.ui = Ui_TaskProperties()
        self.ui.setupUi(self)
        
        # get data for task and fill in form
        self.ui.nameEntry.setText(self.data['name'] if 'name' in self.data else '')

        # connect buttons
        self.ui.discardButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.saveProperties)
    def saveProperties(self, event):
        self.backendInterface.saveTask({'name': self.ui.nameEntry.text(), 'id': self.taskId})
        self.close()
    def addStatus(self, event):
        pass
    def deleteStatus(self, event):
        pass
    def modifyStatus(self, event):
        pass
    def addSchedule(self, event):
        pass
    def deleteSchedule(self, event):
        pass
    def modifySchedule(self, event):
        pass

def main():
    app = QApplication(sys.argv)

    mw = MainWindow(BackendInterface)
    mw.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
