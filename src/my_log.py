import codecs
import time

debug_switch_on = 1 
log_file_name = "../log/RSS2Kindle.log"


def debug_print(str):
    if debug_switch_on == 1:
        print str
    if debug_switch_on == 2:
        write_to_log_file(str)

def write_to_log_file(str):
    log_file = codecs.open(log_file_name, 'a+','utf-8')
    log_file.write(time.ctime()+'   '+str+'\n')
    log_file.close()
