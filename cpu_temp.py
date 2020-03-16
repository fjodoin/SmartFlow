#!/usr/bin/python
import time, sys, json
from random import randint, seed
seed(1)
while(True):
    lognumber = randint(0, 100)
    logdict = {
        'temperature': lognumber
    }
    logstring = json.dumps(logdict)
    with open("/home/corelee/Desktop/winter2020/coen490/events_log.log", "a") as logfile:
        logfile.write(str(logstring) + "\n")
    logfile.close()
    time.sleep(5)
sys.exit()
