import sys
import time as stime
import sort_util
import pickle

from datetime import datetime, time
from functools import partial
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import time as stime
import sort_util
import pickle
import telegram
import configparser

# INI 설정 파일 불러오기
config = configparser.ConfigParser()
config.read('Config.ini')
TeleVarlist = config['TelegramVar']
GlobalVarlist = config['GlobalVar']

# 설정 파일에서 Token,ID 받아오기
token = TeleVarlist['Token']
ID = TeleVarlist['ID']

# 텔레그램 봇에 token 변수에 저장한 토큰값 전송
bot = telegram.Bot(token=token) 

# 언어 선택을 위한 설정값 불러오기
LanguageFlag = GlobalVarlist['Language']

if LanguageFlag == 'English' :
    MustNumber = 'Please enter a "number" in hours or minutes.'
    UnderNumber = 'Please enter a number less than 11 in hours and a number less than 59 in minutes.'
else:
    MustNumber = '시간 or 분에 숫자를 입력해주세요.'
    UnderNumber = '시간에 11 이하의 숫자, 분에 59이하의 숫자를 입력해주세요.'


sub_ui = uic.loadUiType('_uiFiles/sub.ui')[0]

class TimeThread(QThread):
    """
    시간을 설정하는 쓰레드
    """
    
    messagebox = pyqtSignal()
    latest_time_hour = 0
    latest_time_minute = 0

    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def latest_task_time(self,sort_task_list):
        # sort_task_list의 첫 번쨰 키를 : 스플릿 함
        latest_time_keys = list(list(sort_task_list[0].values())[0].keys())[0].split(':')

        date_y_m_d = list(sort_task_list[0].keys())[0].split(':')
        self.latest_time_year = int(date_y_m_d[0])
        self.latest_time_month = int(date_y_m_d[1])
        self.latest_time_day = int(date_y_m_d[2])
        

        # self.am_pm_toggle_value가 PM 이면 12를 더해줘여함 datetime에서 1시는 13시로 표현함
        if latest_time_keys[0] == 'PM':
            if not latest_time_keys[1] == '12':
                self.latest_time_hour = int(latest_time_keys[1]) + 12
            self.latest_time_minute = int(latest_time_keys[2])
        # AM 12시는 datetime에서 0시로 표현
        elif latest_time_keys[0] == 'AM' and latest_time_keys[1] == '12':
            self.latest_time_hour = 0
        else:
            self.latest_time_hour = int(latest_time_keys[1])
            self.latest_time_minute = int(latest_time_keys[2])

        return self.latest_time_hour, self.latest_time_minute, self.latest_time_year, self.latest_time_month, self.latest_time_day

    # TimeThread를 .start() 를하면 실행되는 함수
    def run(self):
        sort_task_list = []
        while True:
            with open("task.pkl", "rb") as f:
                while True:
                    try:
                        sort_task_list = pickle.load(f)
                    except EOFError:
                        break
            
            if sort_task_list :
                # 제일 처음 task의 시간, 분 을 받아옴
                hour, minute, year, month, day = self.latest_task_time(sort_task_list)
                # 현재 시간 분을 받아옴
                now_hour = datetime.today().time().hour
                now_minute = datetime.today().time().minute
                now_year = datetime.today().year
                now_month = datetime.today().month
                now_day = datetime.today().day

                stime.sleep(2)
                if year == now_year and month == now_month and day == now_day:
                    # 현재시각을 task_list 제일 처음의 시각을 받아서 비교해서 시간과 분이 같으면 메세지 실행
                    if now_hour == hour and now_minute == minute:
                        # 메인 view에서 messagebox와 connect와 연결된 함수를 싱햄
                        self.messagebox.emit()
                        # os.system('open /Users/goseonghyeon/study/ScheduleManagement/black.mp3')
                        stime.sleep(0.5)
                        sort_task_list.pop(0)
                        with open("task.pkl", 'wb') as f:
                            pickle.dump(sort_task_list, f)

                    if hour < now_hour :
                        sort_task_list.pop(0)
                        with open("task.pkl", 'wb') as f:
                            pickle.dump(sort_task_list, f)
                    if hour <= now_hour and minute < now_minute :
                        sort_task_list.pop(0)
                        with open("task.pkl", 'wb') as f:
                            pickle.dump(sort_task_list, f)
                
                    
                elif year < now_year :
                    sort_task_list.pop(0)
                    with open("task.pkl", 'wb') as f:
                        pickle.dump(sort_task_list, f)
                elif month < now_month :
                    sort_task_list.pop(0)
                    with open("task.pkl", 'wb') as f:
                        pickle.dump(sort_task_list, f)
                elif day < now_day :
                    sort_task_list.pop(0)
                    with open("task.pkl", 'wb') as f:
                        pickle.dump(sort_task_list, f)


class DayManagement(QWidget, sub_ui):
    am_pm_toggle_value = 'PM'
    task_list = []

    def __init__(self, parent=None):
        super(DayManagement, self).__init__(parent)
        # 시작할때 initUI를 불러온다
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.setWindowTitle(' To_do_list')
        self.setWindowIcon(QIcon('image/icon.png'))

        self.task_save_button.clicked.connect(self.task_save)
        self.am_or_pm_toggle_button.setCheckable(True)
        self.am_or_pm_toggle_button.clicked.connect(self.am_pm_toggle)
 
    def see_task_list(self):
        '''
        새로운 윈도우 창을 여는 함수로 TaskList를 불러와서 show 새로운 창을 염
        '''
        self.see_task_new_window = TaskList()
        self.see_task_new_window.show()

    def task_save(self):
        '''
        시간과 할일 목록을 저장하는 함수
        '''
        with open("task.pkl", "rb") as f:
            sort_task_list = []
            while True:
                try:
                    sort_task_list = pickle.load(f)
                except EOFError:
                    break

        if self.time_check(self.am_pm_toggle_value, self.set_time_hours.text(), self.set_time_minutes.text()):
            # am_pm을 받고 ap_or_pm:시간:분 저장
            year_month_day = "{year}:{month}:{day}:{week}".format(year = self.text_year.text(),
                                                                  month = self.text_month.text(),
                                                                  day = self.text_day.text(),
                                                                  week = self.text_week.text())

            hours_minutes = "{am_or_pm}:{hours}:{minutes}".format(am_or_pm=self.am_pm_toggle_value,
                                                                  hours=self.set_time_hours.text(),
                                                                  minutes=self.set_time_minutes.text())

            # am_or_pm:시간:분 : 할일 해서 딕셔너리로 저장
            time_and_task = {hours_minutes : self.set_task_text.toPlainText()}
            overall_task = {year_month_day : time_and_task}
            
            # 시간과 할일을 task_list에 저장한다
            sort_task_list.append(overall_task)
            sort_task_list = sort_util.date_sort(sort_task_list)

            with open("task.pkl", 'wb') as f:
                pickle.dump(sort_task_list, f)

            # 시간과 할일을 저장 후에 text 칸을 clear 시킨다
            self.set_time_hours.clear()
            self.set_time_minutes.clear()
            self.set_task_text.clear()

        else:
            pass


    def open_message_box(self):
        with open("task.pkl", "rb") as f:
            while True:
                try:
                    sort_task_list = pickle.load(f)
                except EOFError:
                    break
                    
        taskstring=list(list(sort_task_list[0].values())[0].values())[0]
        # 사용자 id 에 종합 변수에 지정한 텍스트 전송
        bot.sendMessage(chat_id = ID, text=taskstring)

        # sort_task_list의 첫
        # alert은 밑에 알림창을 울리게 함 그리고 이 메시지 박스는 내가 보고 있는 화면에 띄워짐
        QApplication.alert(QMessageBox.about(self, 'Message', '{time}\n{task}'.format( \
                                            time=list(list(sort_task_list[0].values())[0].keys())[0],
                                            task=list(list(sort_task_list[0].values())[0].values())[0])))

    def am_pm_toggle(self, toggle):
        '''
        self.am_or_pm_toggle_button을 클릭하면 실행되는 함수로 AM PM을 설정한다
        '''
        if toggle:
            # am_or_pm_toggle_buotton버튼의 텍스를 AM으로 변경
            self.am_or_pm_toggle_button.setText('AM')
            self.am_pm_toggle_value = 'AM'
        else:
            # am_or_pm_toggle_buotton버튼의 텍스를 PM으로 변경
            self.am_or_pm_toggle_button.setText('PM')
            self.am_pm_toggle_value = 'PM'

    def time_check(self, am_pm, hour, minute):
        # 현재 시간을 받아옴
        now_hour, now_minute = datetime.today().time().hour, datetime.today().time().minute
        # hour, minute가 숫자인지 검사
        if not hour.isdigit() or not minute.isdigit() or hour == '' or minute == '':
            QMessageBox.about(self, 'Error', MustNumber)
            return False
        elif int(hour) > 11 or int(minute) >= 60:
            QMessageBox.about(self, 'Error', UnderNumber)
            return False
        elif am_pm == 'PM':
            # 오후 시간에는 시간이 느리면 저장 불가능
            # am을 안한 이유는 밤에 작업할때 11:00에 작업중이면 그 다음날 새벽 까지도 작업할 수 있기 때문에 am은 제외
            if not hour == '12':
                hour = int(hour) + 12
            # if time(int(hour), int(minute)) < datetime.today().time():
            #     QMessageBox.about(self, 'Error', '{}:{}이후의 시간을 입력해주세요.'.format(now_hour, now_minute))
            #     return False
            else:
                return True
        return True

