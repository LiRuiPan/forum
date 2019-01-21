import time


def log(*args, **kwargs):
    time_format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, **kwargs)
        print(dt, *args, file=f, **kwargs)
