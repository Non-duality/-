import sys, pickle, sort_util
import configparser
from datetime import datetime, time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

# INI 설정 파일 불러오기
config = configparser.ConfigParser()
config.read('Config.ini')
GlobalVarlist = config['GlobalVar']

# 전역 설정값 가져오기
GlobalVarlist = config['GlobalVar']

# 언어 선택을 위한 설정값 불러오기
LanguageFlag = GlobalVarlist['Language']

if LanguageFlag == 'English' :
    modify_sub = uic.loadUiType("_uiFiles/modify_sub_eng.ui")[0]
    Titlename = "Edit To Do List"
    QUIT = "QUIT"
    QUITMESSAGE = "Save Changes?"
else:
    modify_sub = uic.loadUiType("_uiFiles/modify_sub.ui")[0]
    Titlename = "일정 목록 수정"
    QUIT = "나가기"
    QUITMESSAGE = "변경 사항을 저장 하시겠습니까?"
    
check = False

class ModifyList(QListWidget, modify_sub) :
    def __init__(self) :
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setupUi(self)

        self.setWindowTitle(Titlename)
        self.setWindowIcon(QIcon('image/icon.png'))

        #ListWidget의 시그널
        self.list_widget.itemClicked.connect(self.chkItemClicked)

        #버튼에 기능 연결
        self.btn_modify_item.clicked.connect(self.modifyListWidget)
        self.btn_removeItem.clicked.connect(self.removeCurrentItem)
        self.btn_clearItem.clicked.connect(self.clearItem)
        self.btn_saveItem.clicked.connect(self.save_to_do_list)

    def chkItemClicked(self) :
        self.line_modify_item.setText(self.list_widget.currentItem().text())
    
    def modifyListWidget(self):
        self.modify_ItemText = self.line_modify_item.text()
        self.list_widget.currentItem().setText(self.modify_ItemText)
        self.line_modify_item.clear()

    def removeCurrentItem(self) :
        #ListWidget에서 현재 선택한 항목을 삭제할 때는 선택한 항목의 줄을 반환한 후, takeItem함수를 이용해 삭제합니다. 
        self.removeItemRow = self.list_widget.currentRow()
        self.list_widget.takeItem(self.removeItemRow)

    def clearItem(self) :
        self.list_widget.clear()
    
    def add_to_do_list(self):

        self.list_widget.clear()
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
                month = date_y_m_d[1]
                day = date_y_m_d[2]
                week = date_y_m_d[3]
                
                temp_date = "{year}.{month}.{day}.{week}".format(year = year, month = month, day = day,
                                                                 week = week)
                
                temp_time = list(list(task.values())[0].keys())[0]
                temp_task = list(list(task.values())[0].values())[0]

                total_temp = temp_date + " " + temp_time + " " + temp_task
                self.list_widget.addItem(total_temp)

        else:
            pass
    
    def save_to_do_list(self):
        global check
        sort_task_list = []
        item_list = []
        if self.list_widget.count() > 0:
            for index in range(self.list_widget.count()):
                item_list = self.list_widget.item(index).text().split(" ")
                date_list = item_list[0].split(".")

                year_month_day = "{year}:{month}:{day}:{week}".format(year = date_list[0],
                                                                    month = date_list[1],
                                                                    day = date_list[2],
                                                                    week = date_list[3])

                time_and_task = {item_list[1] : item_list[2]}
                overall_task = {year_month_day : time_and_task}
                
                sort_task_list.append(overall_task)
                sort_task_list = sort_util.date_sort(sort_task_list)

                with open("task.pkl", 'wb') as f:
                    pickle.dump(sort_task_list, f)
                check = True

        else:
            with open("task.pkl", 'wb') as f:
                pickle.dump(sort_task_list, f)
            check = True
    
    def closeEvent(self, event):
        global check
        if check:
            check = False
            event.accept()
        else:
            close = QMessageBox.question(self,
                                        QUIT,
                                        QUITMESSAGE,
                                        QMessageBox.Yes | QMessageBox.No)
            if close == QMessageBox.Yes:
                self.save_to_do_list()
                check = False
                event.accept()
            else:
                event.accept()