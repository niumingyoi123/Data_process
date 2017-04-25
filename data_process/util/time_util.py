import time
def t(s):
    l=time.mktime(time.strptime(s,'%Y-%m-%d %H:%M:%S'))
    return l/1000/60