import sys
import pickle

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from DayManagement import *
sort_task_list = []
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
        self.calendarWidget.clicked[QDate].connect(self.show_data)
        date = self.calendarWidget.selectedDate()
        self.pushButton.clicked.connect(self.clicked_option)

        self.show_data(date)

    def sort_date(self,date):
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
    
    def show_data(self,date):
        # Label에 데이터를 기록하는 함수
        temp = self.splitDate(date)
        task_str = ""

        self.time_label.setText(self.sort_date(date))
        
        if self.select_task(date):
            for task in self.select_task(date):
                task_str = task_str + task + "\n"
            self.task_label.setText(task_str)
        
        else:
            self.task_label.setText("일정 없음")

        self.new_window.text_year.setText(temp[3])
        self.new_window.text_month.setText(temp[1])
        self.new_window.text_day.setText(temp[2])
        self.new_window.text_week.setText(temp[0])
    
    def select_task(self, date):
        global sort_task_list
        temp = self.splitDate(date)
        temp_task_list = []
        task_list = []

        with open("task.pkl", "rb") as f:
            while True:
                try:
                    sort_task_list = pickle.load(f)
                except EOFError:
                    break
        
        if sort_task_list:
            for task in sort_task_list:
                date_y_m_d = list(task.keys())[0].split(':')
                year = int(date_y_m_d[0])
                month = int(date_y_m_d[1])
                day = int(date_y_m_d[2])
            
                if int(temp[3]) == year and int(temp[1]) == month and int(temp[2]) == day :
                    #시간 데이터 담기
                    temp_time = list(list(task.values())[0].keys())[0]
                    #일정 데이터 담기
                    temp_task_list = list(list(task.values())[0].values())[0].split(':')
                    temp_time = "[ " + temp_time + " ] "
                    temp_time = temp_time + temp_task_list[0]
                    temp_task_list.pop(0)
                    temp_task_list.append(temp_time)

                    print(temp_task_list)
                    task_list.append(temp_task_list[0])
                    temp_task_list.pop(0)

        else:
            return task_list
        
        return task_list
        





if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = MainWindow()
    main_dialog.show()
    app.exec_()