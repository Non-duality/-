from datetime import time, datetime

def sort_key_dict_fuction(task):
    '''
    task_list에 key를 뺴와서 time으로 리턴해서 sort 하는 함수
    '''
    # task의 keys를[0] :를 기준으로 나눠서 am_pm, hour, minute
    date_y_m_d = list(task.keys())[0].split(':')
    year = int(date_y_m_d[0])
    month = int(date_y_m_d[1])
    day = int(date_y_m_d[2])

    time_h_s = list(list(task.values())[0].keys())[0].split(':')
    AM_PM = time_h_s[0]

    if AM_PM == 'PM':
        hour = int(time_h_s[1]) + 12
        minute = int(time_h_s[2])
    else:
        hour = int(time_h_s[1])
        minute = int(time_h_s[2])
    
    return datetime(year,month,day,hour,minute)

def date_sort(task_list):
    
    for task in task_list :
        task_list.sort(key=sort_key_dict_fuction)
    return task_list