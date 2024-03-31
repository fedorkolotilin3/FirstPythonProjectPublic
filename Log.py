log_file = None
def f_open():
    global log_file
    log_file = open("main_log.txt", 'a')
def print(string, end='\n'):
    global log_file
    f_open()
    log_file.write(str(string) + end)
    close()
def close():
    global log_file
    log_file.close()