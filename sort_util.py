from datetime import time, datetime

def sort_key_dict_fuction(task):
    '''
    task_list에 key를 뺴와서 time으로 리턴해서 sort 하는 함수
    '''
    # task의 keys를[0] :를 기준으로 나눠서 am_pm, hour, minute
    time_h_s = list(task.keys())[0].split(':')
    hour = int(time_h_s[1])
    minute = int(time_h_s[2])
    return time(hour, minute)


def task_list_sort(task_list):
    """
    task_list 를 pm, am으로 리스트를 나누어서 정렬함
    """
    pm_task_list = []
    am_task_list = []
    # am 은 pm을 나눠서 각 리스트에 정렬
    for task in task_list:
        task_am_or_pm = list(task.keys())[0].split(':')[0]
        if task_am_or_pm == 'PM':
            pm_task_list.append(task)
        elif task_am_or_pm == 'AM':
            am_task_list.append(task)

    # pm_task_list == [] 이면 am_task_list만 출력
    if pm_task_list == []:
        am_task_list.sort(key=sort_key_dict_fuction)
        return am_task_list
    # am_task_list == [] 이면 pm_task_list만 출력
    elif am_task_list == []:
        pm_task_list.sort(key=sort_key_dict_fuction)
        return pm_task_list
    # 12시 이상이면 pm_task_list 가 먼저 옴
    elif datetime.today().time().hour >= 12:
        am_task_list.sort(key=sort_key_dict_fuction)
        pm_task_list.sort(key=sort_key_dict_fuction)
        return pm_task_list + am_task_list
    else:
        am_task_list.sort(key=sort_key_dict_fuction)
        pm_task_list.sort(key=sort_key_dict_fuction)
        return am_task_list + pm_task_list