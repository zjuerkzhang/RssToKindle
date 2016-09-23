import ConfigParser
import my_log
import os
import time

config_ini_file = "../config/rss_time.ini"
section_name = "timestamp"

def getStoredTimestamp(key):
    if not os.path.exists(config_ini_file):
        os.system('echo [%s] > %s' % (section_name, config_ini_file))
    config = ConfigParser.ConfigParser()
    try:
        config.readfp(open(config_ini_file))
    except Exception:            
        my_log.write_to_log_file('<--Error-->: Fail to read INI file %s' % config_ini_file)
        return ''
    try:
        last_time = config.get(section_name, key)
    except Exception:
        my_log.write_to_log_file('<--Error-->: Fail to read section %s and key %s' % (section_name, key))
        time_now = time.strftime("%Y%m%d%H%M%S")
        os.system('echo "%s = %s" >> %s' % (key, time_now, config_ini_file))
        return time_now
    return last_time  

def updateStoredTimestamp(key, timestamp):
    config = ConfigParser.ConfigParser()
    try:
        config.readfp(open(config_ini_file))
    except Exception:            
        my_log.write_to_log_file('<--Error-->: Fail to read INI file %s' % config_ini_file)
        return 
    config.set(section_name, key, timestamp)
    config.write(open(config_ini_file, "r+"))   
    my_log.debug_print('******Update the ' + key + "'s" + ' timestamp [' + timestamp + '] ************')
    return 

if __name__ == '__main__':
    print getStoredTimestamp('TEST_TS')
    updateStoredTimestamp('TEST_TS', '20550102030405')
    print getStoredTimestamp('TEST_TS')
