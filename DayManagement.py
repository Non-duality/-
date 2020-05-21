import sys
from datetime import datetime, time
from functools import partial
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QRect
from PyQt5.QtWidgets import *
from main import MainWindow as mw
import time as stime
import sort_util

sort_task_list = []


class TimeThread(QThread):
    """
    시간을 설정하는 쓰레드
    """
    # 일반적으로 pyqt5에서는 메인 쓰레드가 아닌 경우에는 pyqt5의 messagebox나 새로운 윈도우창을 키는 행동을 할수가 없다
    # 그래서 message 박스를 불러오는 통로 같은것을 만드는 것

    messagebox = pyqtSignal()
    latest_time_hour = 0
    latest_time_minute = 0

    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def latest_task_time(self):
        global sort_task_list
        # task_list의 첫 번쨰 키를 : 스플릿 함
        latest_time_keys = list(sort_task_list[0].keys())[0].split(':')
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

        return self.latest_time_hour, self.latest_time_minute

    # TimeThread를 .start() 를하면 실행되는 함수
    def run(self):
        global sort_task_list
        # 시간을 체크함
        while True:
            print(sort_task_list)
            if sort_task_list == []:
                break
            # 제일 처음 task의 시간, 분 을 받아옴
            hour, minute = self.latest_task_time()
            # 현재 시간 분을 받아옴
            now_hour = datetime.today().time().hour
            now_minute = datetime.today().time().minute
            stime.sleep(30)
            # 현재시각을 task_list 제일 처음의 시각을 받아서 비교해서 시간과 분이 같으면 메세지 실행
            if now_hour == hour and now_minute == minute:
                # print(datetime.today().time())
                # print(time(hour,minute))
                # 메인 view에서 messagebox와 connect와 연결된 함수를 싱햄
                self.messagebox.emit()
                # os.system('open /Users/goseonghyeon/study/ScheduleManagement/black.mp3')
                stime.sleep(0.5)
                sort_task_list.pop(0)


class DayManagement(QWidget):
    am_pm_toggle_value = 'PM'
    task_list = []
    thread_count = 0

    def __init__(self, parent=None):
        super(DayManagement, self).__init__(parent)
        # 시작할때 initUI를 불러온다
        self.initUI()

    def initUI(self):
        # 레이아웃은 그리드 레이아웃으로 설정
        grid = QGridLayout()

        # AM_PM_toggle
        # AM 과 PM을 설정하기 위한 토글 라벨을 설정한다
        am_or_pm_toggle_label = QLabel("AM PM Toggle")
        am_or_pm_toggle_label.setAlignment(Qt.AlignCenter)
        # AM 과 PM을 설정하기 위해서 버튼을 만든다
        self.am_or_pm_toggle_button = QPushButton("PM")

        # am_or_pm_toggle_label을 grid 레이아웃에 1행에 0열에 설정
        grid.addWidget(am_or_pm_toggle_label, 1, 0)

        # am_or_pm_toggle_button을 grid 레이아웃에 2행에 0열에 설정
        grid.addWidget(self.am_or_pm_toggle_button, 2, 0)
        # am_or_pm_toggle_button을 토글 버튼으로 만든다
        self.am_or_pm_toggle_button.setCheckable(True)

        # TIME 설정
        # 시간을 설정하기 위한 시간 라벨을 설정한다
        set_time_label = QLabel('TIME')
        # set_time_label을 중간으로 설정한다
        set_time_label.setAlignment(Qt.AlignCenter)
        # set_time_label을 grid 레이아웃에 3행 0열에 설정
        grid.addWidget(set_time_label, 3, 0)

        # 수평에 대한 레이아웃 생성
        self.set_time_layout = QHBoxLayout()
        # 중앙을 맞추기 위한 왼쪽 공백 생성
        self.set_time_layout.addStretch()
        # 시간, 분 을 받기위한 텍스트
        self.set_time_hours = QLineEdit()
        self.set_time_minutes = QLineEdit()
        # 시간, 분 텍스트 사이즈 조정
        self.set_time_hours.setMaximumSize(25, 20)
        self.set_time_minutes.setMaximumSize(25, 20)
        # 시간, 분 수평 레이아웃(set_time_layout) 집어넣어 설정함
        self.set_time_layout.addWidget(self.set_time_hours)
        self.set_time_layout.addWidget(QLabel(':'))
        self.set_time_layout.addWidget(self.set_time_minutes)
        # 중앙을 맞추기 위한 오른쪽 공백 생성
        self.set_time_layout.addStretch()

        # set_time_layout를 grid레이아웃에 추가함
        grid.addLayout(self.set_time_layout, 4, 0)

        # task 라벨 추가
        self.set_task_text_label = QLabel("TASK")
        # set_task_text_label 중앙 정렬
        self.set_task_text_label.setAlignment(Qt.AlignCenter)
        # grid 레이아웃에 5행에 정렬
        grid.addWidget(self.set_task_text_label, 5, 0)
        # task 내용 text 설정
        self.set_task_text = QTextEdit()
        # grid 레이아웃에 task text 6행에 정렬
        grid.addWidget(self.set_task_text, 6, 0)

        # 시간과 할일을 저장하는 save 버튼
        self.task_save_button = QPushButton("save")
        # task_save_button을 def task_save 함수랑 연결
        self.task_save_button.clicked.connect(self.task_save)
        # self.task_save_button을 gird 레이아웃에 7행에 정렬
        grid.addWidget(self.task_save_button, 7, 0)

        # 지금까지 저장한 task 목록을 보여주는 버튼
        self.see_task_list_button = QPushButton("task list")
        # see_task_list 함수랑 see_task_list_button 버튼을 연결
        self.see_task_list_button.clicked.connect(self.see_task_list)
        # see_task_list_button 8행에 정렬
        grid.addWidget(self.see_task_list_button, 8, 0)
        # am_or_pm_toggle_button을 클릭하면 self.am_pm_toggle함수를 실행한다
        self.am_or_pm_toggle_button.clicked.connect(self.am_pm_toggle)

        self.setLayout(grid)
        self.setGeometry(300, 300, 540, 300)

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
        global sort_task_list
        if self.time_check(self.am_pm_toggle_value, self.set_time_hours.text(), self.set_time_minutes.text()):
            # am_pm을 받고 ap_or_pm:시간:분 저장
            hours_minutes = "{am_or_pm}:{hours}:{minutes}".format(am_or_pm=self.am_pm_toggle_value,
                                                                  hours=self.set_time_hours.text(),
                                                                  minutes=self.set_time_minutes.text())
            # am_or_pm:시간:분 : 할일 해서 딕셔너리로 저장
            time_and_task = {hours_minutes: self.set_task_text.toPlainText()}
            
            # 시간과 할일을 task_list에 저장한다
            sort_task_list.append(time_and_task)
            sort_task_list = sort_util.task_list_sort(sort_task_list)
            # 시간과 할일을 저장 후에 text 칸을 clear 시킨다
            self.set_time_hours.clear()
            self.set_time_minutes.clear()
            self.set_task_text.clear()
            # 쓰레드는 한 번만 실행되면 되기 떄문에 카운트가 0일 때만 실행 또는 하나만 있을 떄만 실행
            if self.thread_count == 0 or len(sort_task_list) == 1:
                print(self.thread_count)
                print(len(self.task_list))
                # TimeThread을 할당
                self.time_check_thread = TimeThread()
                # 메인 쓰레드가 종료되면 자식 쓰레드인 self.time_check_thread 종료
                self.time_check_thread.daemon = True
                # TimeThread에 있는 messagebox 시그널과 연결
                self.time_check_thread.messagebox.connect(self.open_message_box)
                # 쓰레드 실행
                self.time_check_thread.start()
                # 한 번만 실행되야 하기때문에 수를 올림
                self.thread_count += 1
        else:
            pass

    def open_message_box(self):
        global sort_task_list
        # alert은 밑에 알림창을 울리게 함 그리고 이 메시지 박스는 내가 보고 있는 화면에 띄워짐
        QApplication.alert(QMessageBox.about(self, 'Message', '{time}\n{task}'.format( \
                                            time=list(sort_task_list[0].keys())[0],
                                            task=list(sort_task_list[0].values())[0])))

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
            QMessageBox.about(self, 'Error', '시간 or 분에 숫자를 입력해주세요.')
            return False
        elif int(hour) > 12 or int(minute) >= 60:
            QMessageBox.about(self, 'Error', '시간에 12 이하의 숫자, 분에 59이하의 숫자를 입력해주세요.')
            return False
        elif am_pm == 'PM':
            # 오후 시간에는 시간이 느리면 저장 불가능
            # am을 안한 이유는 밤에 작업할때 11:00에 작업중이면 그 다음날 새벽 까지도 작업할 수 있기 때문에 am은 제외
            if not hour == '12':
                hour = int(hour) + 12
            if time(int(hour), int(minute)) < datetime.today().time():
                QMessageBox.about(self, 'Error', '{}:{}이후의 시간을 입력해주세요.'.format(now_hour, now_minute))
                return False
            else:
                return True
        return True


class TaskList(QWidget):
    '''
    할일 목록을 보여주는 새로운 윈도우 클래스
    '''
    # 할일 목록을 할당
    global sort_task_list
    # 수정할 때 인덱스를 이용해서 수정하기 위해 모든 ui를 딕으로 만듬
    task_list_wrap_layout = {}
    task_list_top_layout = {}
    task_list_button_layout = {}
    task_time_hours = {}
    task_time_minutes = {}
    am_or_pm_toggle_button = {}
    text = {}
    task_list_delete_button = {}
    task_list_modified_button = {}

    def __init__(self):
        super().__init__()
        # 스크롤 전체 지역을 설정함
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        # 그리드 레이아웃을 감쌀 전체 레이아웃을 설정
        wrap_layout = QHBoxLayout(self)
        # scroll안에 들어갈 요소 설정할 위젯 생성
        self.scrollAreaWidgetContents = QWidget()
        # 그리드 레이아웃에 스크롤 요소가 들어갈 수 있음
        self.grid = QGridLayout(self.scrollAreaWidgetContents)
        # scroll에 설정해줘야 위젯이 나옴
        scroll.setWidget(self.scrollAreaWidgetContents)
        scroll.resize(300, 800)
        # 할일 목록 하나당 배정함
        for index, work in enumerate(sort_task_list):
            # 각 할 일 마다 am_or_pm, hours, minutes 구함
            am_or_pm, hours, minutes = list(work.keys())[0].split(':')
            # 할 일을 구함
            task = list(work.values())[0]
            # 모든 레이아웃을 감쌀 수직 레이아웃
            self.task_list_wrap_layout[index] = QVBoxLayout()
            # ex)AM:시간:분을 감싸는 수평 레이아웃
            self.task_list_top_layout[index] = QHBoxLayout()
            # 삭제, 수정 버튼을 감싸는 수평 레이아웃
            self.task_list_button_layout[index] = QHBoxLayout()

            # 시간, 분을 넣을 text창
            self.task_time_hours[index] = QLineEdit()
            self.task_time_minutes[index] = QLineEdit()
            
            

            # task의 PM이면 토글버튼에 PM, AM이면 AM 설정
            if am_or_pm == 'PM':
                self.am_or_pm_toggle_button[index] = QPushButton("PM")
            elif am_or_pm == 'AM':
                self.am_or_pm_toggle_button[index] = QPushButton("AM")
            # am_or_pm_toggle_button을 토글버튼으로 만듬
            self.am_or_pm_toggle_button[index].setCheckable(True)

            # am_or_pm_toggle_button을 self.am_pm_toggle 함수랑 연경하고 index를 인자로 줌
            self.am_or_pm_toggle_button[index].clicked.connect(partial(self.am_pm_toggle, index))
            # hours을 task_time_hours을 text창에 할당, minutes을 task_time_minutes을 text 창에 할당
            self.task_time_hours[index].setText(hours)
            self.task_time_minutes[index].setText(minutes)

            # 크기 조정
            self.task_time_hours[index].setMaximumSize(25, 20)
            self.task_time_minutes[index].setMaximumSize(25, 20)

            # task_list_top_layuout에 ex)AM:hour:minute을 설정
            self.task_list_top_layout[index].addWidget(self.am_or_pm_toggle_button[index])
            self.task_list_top_layout[index].addWidget(self.task_time_hours[index])
            self.task_list_top_layout[index].addWidget(QLabel(":"))
            self.task_list_top_layout[index].addWidget(self.task_time_minutes[index])

            # task_list_top_layout오른쪾에 빈 공간을 만듬
            self.task_list_top_layout[index].addStretch()

            # 큰 text 창을 생성
            self.text[index] = QTextEdit()
            # task를 text에 할당
            self.text[index].setPlainText(task)

            # 삭제, 수정 버튼
            self.task_list_delete_button[index] = QPushButton('Delete')
            self.task_list_modified_button[index] = QPushButton('Modified')

            # 수정 버튼을 task_modified 함수에 할당 인자를 주기위해 partial 사용
            self.task_list_modified_button[index].clicked.connect(partial(self.task_modified, index))
            self.task_list_delete_button[index].clicked.connect( \
                partial(self.task_delete, self.task_list_wrap_layout[index], list(work.keys())[0], True))

            # task_list_button_lalyout에 삭제, 수정 버튼을 추가
            self.task_list_button_layout[index].addWidget(self.task_list_delete_button[index])
            self.task_list_button_layout[index].addWidget(self.task_list_modified_button[index])

            # task_list_wrap_layout(전체를 감싸는 layout)에 task_list_top_layout, text, task_list_button_layout을 추가
            self.task_list_wrap_layout[index].addLayout(self.task_list_top_layout[index])
            self.task_list_wrap_layout[index].addWidget(self.text[index])
            self.task_list_wrap_layout[index].addLayout(self.task_list_button_layout[index])

            # task_list_wrap_layout을 grid레이아웃에 추가
            self.grid.addLayout(self.task_list_wrap_layout[index], index, 0)
        # 전체 레이아웃에 스크롤을 포함
        wrap_layout.addWidget(scroll)
        self.setGeometry(1000, 1, 300, 600)
        self.setLayout(wrap_layout)
        self.show()

    def am_pm_toggle(self, index, toggle):
        '''
        self.am_or_pm_toggle_button을 클릭하면 실행되는 함수로 AM PM을 설정한다
        '''
        # toggle 순서가 가장 마지막이라서 index를 두번쨰에 줘야함 안그러면 index가 토글 역할을 해버림
        if toggle:
            # am_or_pm_toggle_buotton버튼의 텍스를 AM으로 변경
            self.am_or_pm_toggle_button[index].setText('AM')
        else:
            # am_or_pm_toggle_buotton버튼의 텍스를 PM으로 변경
            self.am_or_pm_toggle_button[index].setText('PM')

    def task_modified(self, index):
        global sort_task_list
        # 수정할 task를 받음
        # 키를 변경하기 위해 현재 시간 반환
        old_task_time = list(sort_task_list[index].keys())[0]
        # self.am_or_pm_toggle_button_button의 텍스트를 들고와서 ap 또는 pm을 설정
        am_or_pm = self.am_or_pm_toggle_button[index].text()
        # task_list는 dict 구조라서 새로운 key를 만듬
        modified_task_time = "{am_or_pm}:{hours}:{minutes}".format(am_or_pm=am_or_pm,
                                                                   hours=self.task_time_hours[index].text(),
                                                                   minutes=self.task_time_minutes[index].text())
        # dict에서 key를 변경해줄때 기존의 dict[새로운key] = dict.pop(기존key)를 하면 키가 바꿔짐
        # [index][modified_task_time]을 하면 이중구조로 되는줄 알았는데 sort_task_list[index]의 키를 들고옴
        sort_task_list[index][modified_task_time] = sort_task_list[index].pop(old_task_time)
        sort_task_list[index][modified_task_time] = self.text[index].toPlainText()
        #  배열이 바뀌었기 때문에 재 배열 해줘여함
        sort_task_list = sort_util.task_list_sort(sort_task_list)
        # 수정했을떄 페이지를 갱신함
        self.close()
        TaskList().show()

    def task_delete(self, layout, key, remove):
        global sort_task_list
        # task_list[index]를 한 번만 삭제시키기 remove=True 일떄만 삭제
        if remove:
            # key를 이용해서 리스트안에 있는 딕을 제거
            # 이유는 a(0),b(1),c(2) 가 있을때 b를 지우면 a(0),c(1) 되지만 나의 메모리에서는 c의 인덱스가 2라고 저장 되어있기떄문
            for index, task in enumerate(sort_task_list):
                if key == list(task.keys())[0]:
                    del sort_task_list[index]
        # layout자체를 삭제 할 수 없으므로 안에 아이템을 삭제 해야함
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.task_delete(item.layout(), key, remove=False)
                    # 레이아웃 재 설정
