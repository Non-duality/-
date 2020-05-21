import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from DayManagement import *


main_ui = uic.loadUiType('_uiFiles/main.ui')[0]

class MainWindow (QMainWindow, main_ui):
    global sort_task_list

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setupUi(self)
        self.setWindowTitle(' Scheldule Management')
        self.setWindowIcon(QIcon('image/icon.png'))
        self.new_window = DayManagement() 

        # 메뉴바
        exitAction = QAction(QIcon('image/exit.png'),'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

        # 클릭 함수
        self.calendarWidget.clicked[QDate].connect(self.showDate)
        self.pushButton.clicked.connect(self.clicked_option) 

        date = self.calendarWidget.selectedDate()
        self.showDate(date)

    
    def clicked_option(self):
        self.new_window.show()
    
    def showDate(self, date):
        temp = date.toString().split(' ')
        time = "{}년 {}월 {}일 {}요일".format(temp[3],temp[1],temp[2],temp[0])
        self.time_label.setText(time)
    
    def test(self,date):
        for index, work in enumerate(sort_task_list):
            # 각 할 일 마다 am_or_pm, hours, minutes 구함
            am_or_pm, hours, minutes = list(work.keys())[0].split(':')
            # 할 일을 구함
            task = list(work.values())[0]
            string = "{} {} : {}\n {}".format(am_or_pm, hours, minutes, task)
            self.task_label.setText(string)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = MainWindow()
    main_dialog.show()
    app.exec_()