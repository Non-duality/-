import sys, pickle, sort_util, configparser, os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtCore
from DayManagement import *
from modify import ModifyList

# INI 설정 파일 불러오기
config = configparser.ConfigParser()
config.read('Config.ini')
GlobalVarlist = config['GlobalVar']

# 전역 설정값 가져오기
GlobalVarlist = config['GlobalVar']

# 언어 선택을 위한 설정값 불러오기
LanguageFlag = GlobalVarlist['Language']

if LanguageFlag == 'English' :
    main_ui = uic.loadUiType('_uiFiles/main_eng.ui')[0]
    Notask = 'There is no task'
    Changelang = "한국어 사용"
else:
    main_ui = uic.loadUiType('_uiFiles/main.ui')[0]
    Notask = '일정 없음'
    Changelang = "To english"
    



class MainWindow (QMainWindow, main_ui):
    thread_count = 0

    
    def __init__(self):
        super().__init__()
        self.initUI()

  
    def initUI(self):
        self.setupUi(self)
        self.setWindowTitle(' Scheldule Management')
        self.setWindowIcon(QIcon('image/icon.png'))
        self.new_window = DayManagement()
        self.new_window_modify = ModifyList()
        self.thread_Start()
        
        # 언어 설정값이 English일 경우 달력 언어 변경
        if LanguageFlag == 'English' :
            self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))

        # 메뉴바
        exitAction = QAction(QIcon('image/exit.png'),'EXIT', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)
        
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&FILE')
        filemenu.addAction(exitAction)
        
        # 클릭 함수
        date = self.calendarWidget.selectedDate()
        self.calendarWidget.clicked[QDate].connect(self.show_data)
        self.pushButton.clicked.connect(self.add_task)
        self.modify_Button.clicked.connect(self.modify_task)
        self.show_data(date)
        
    def ChangeLanguage(self):
        if LanguageFlag == 'English' :
            config["GlobalVar"] = { "Language" : "Korean"};
            config.write(handle);
            #os.system("./main.py &")
        else:
            config["GlobalVar"] = { "Language" : "English"};
            config.write(handle);
            #os.system("./main.py &")

    def thread_Start(self):
        
        if self.thread_count == 0 :
            print(self.thread_count)
            # TimeThread을 할당
            self.time_check_thread = TimeThread()
            # 메인 쓰레드가 종료되면 자식 쓰레드인 self.time_check_thread 종료
            self.time_check_thread.daemon = True
            # TimeThread에 있는 messagebox 시그널과 연결
            self.time_check_thread.messagebox.connect(self.new_window.open_message_box)
            # 쓰레드 실행
            self.time_check_thread.start()
            # 한 번만 실행되야 하기때문에 수를 올림
            self.thread_count += 1

    def sort_date(self,date):
        #Pyqt5.Qtcore.QDate는 데이터를 '월 5 13 2020' 식으로 데이터를 반납한다.
        #그리하여 이를 한국식으로 변환함
        temp = date.toString().split(' ')
        if LanguageFlag == 'English' :
            if temp[0] == "월":
                temp[0] = "Mon"
            elif temp[0] == "화":
                temp[0] = "Tue"
            elif temp[0] == "수":
                temp[0] = "Wed"
            elif temp[0] == "목":
                temp[0] = "Thu"
            elif temp[0] == "금":
                temp[0] = "Fri"
            elif temp[0] == "토":
                temp[0] = "Sat"
            elif temp[0] == "일":
                temp[0] = "Sun"

            time = "{}, {} - {} - {}".format(temp[0],temp[1],temp[2],temp[3])
        else :
            time = "{}년 {}월 {}일 {}요일".format(temp[3],temp[1],temp[2],temp[0])
        return time
    
    def splitDate(self,date):
        temp = date.toString().split(' ')
        return temp

    def add_task(self):
        self.new_window.show()

    def modify_task(self):
        self.new_window_modify.show()
        self.new_window_modify.add_to_do_list()
    
    def show_data(self,date):
        # Label에 데이터를 기록하는 함수
        self.calendarWidget.setDateTextFormat( QDate() , QTextCharFormat() )
        self.paintCell()
        temp = self.splitDate(date)
        task_str = ""

        self.time_label.setText(self.sort_date(date))
        
        if self.select_task(date):
            for task in self.select_task(date):
                task_str = task_str + task + "\n"
            self.task_label.setText(task_str)
        
        else:
            self.task_label.setText(Notask)

        self.new_window.text_year.setText(temp[3])
        self.new_window.text_month.setText(temp[1])
        self.new_window.text_day.setText(temp[2])
        self.new_window.text_week.setText(temp[0])
    
    def select_task(self, date):
        temp = self.splitDate(date)
        task_list = []

        with open("task.pkl", "rb") as f:
            sort_task_list = []
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
                    temp_task = list(list(task.values())[0].values())[0]
                    temp_time = "[ " + temp_time + " ] "
                    temp_time = temp_time + temp_task

                    task_list.append(temp_time)

        else:
            return sort_task_list
        
        return task_list

    def select_event(self):
        event_list = []

        with open("task.pkl", "rb") as f:
            sort_task_list = []
            while True:
                try:
                    sort_task_list = pickle.load(f)
                except EOFError:
                    break
        
        if sort_task_list:
            for task in sort_task_list:
                date_y_m_d = list(task.keys())[0].split(':')
                year = date_y_m_d[0]
                month = date_y_m_d[1].zfill(2)
                day = date_y_m_d[2].zfill(2)

                temp_str = year + month + day
                temp_date = QDate.fromString(temp_str, "yyyyMMdd")
                event_list.append(temp_date)
        
        return event_list
    
    def paintCell(self):
        fm = QTextCharFormat()
        # fm.setForeground(Qt.red)
        fm.setBackground(QColor(204, 235, 255))
        for date in self.select_event():
            self.calendarWidget.setDateTextFormat(date,fm)
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = MainWindow()
    main_dialog.show()
    app.exec_()