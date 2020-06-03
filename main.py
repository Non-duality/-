import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from DayManagement import *

main_ui = uic.loadUiType('_uiFiles/main.ui')[0]

class MainWindow (QMainWindow, main_ui):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setupUi(self)
        self.setWindowTitle(' Scheldule Management')
        self.setWindowIcon(QIcon('image/icon.png'))
        self.new_window = DayManagement() 

        # 메뉴바
        exitAction = QAction(QIcon('image/exit.png'),'EXIT', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&FILE')
        filemenu.addAction(exitAction)

        # 클릭 함수
        self.calendarWidget.clicked[QDate].connect(self.showData)
        date = self.calendarWidget.selectedDate()
        self.pushButton.clicked.connect(self.clicked_option)

        self.showData(date)

    def sortDate(self,date):
        #Pyqt5.Qtcore.QDate는 데이터를 '월 5 13 2020' 식으로 데이터를 반납한다.
        #그리하여 이를 한국식으로 변환함
        temp = date.toString().split(' ')
        time = "{}년 {}월 {}일 {}요일".format(temp[3],temp[1],temp[2],temp[0])
        return time
    
    def splitDate(self,date):
        temp = date.toString().split(' ')
        return temp

    def clicked_option(self):
        self.new_window.show()
    
    def showData(self,date):
        # Label에 데이터를 기록하는 함수
        temp = self.splitDate(date)

        self.time_label.setText(self.sortDate(date))

        self.new_window.text_year.setText(temp[3])
        self.new_window.text_month.setText(temp[1])
        self.new_window.text_day.setText(temp[2])
        self.new_window.text_week.setText(temp[0])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = MainWindow()
    main_dialog.show()
    app.exec_()