import logging
from datetime import datetime
import time
import os

__author__ = 'RaldenProg'


class Logging:
    logging.basicConfig(filename='logger.log',
                        format='%(filename)-12s[LINE:%(lineno)d] %(levelname)-8s %(message)s %(asctime)s ',
                        level=logging.ERROR)


class Debug:
    def create():
        date_now = datetime.now().strftime('%Y.%m.%d %H.%M.%S')
        if not os.path.exists("Debug_files"):
            os.makedirs("Debug_files")
        if not os.path.exists("Debug_files/" + date_now.split()[0]):
            os.makedirs("Debug_files/" + date_now.split()[0])
        if not os.path.exists("Debug_files/" + date_now.split()[0] + "/" + date_now):
            os.makedirs("Debug_files/" + date_now.split()[0] + "/" + date_now)

    def read():
        return "OK"


deb = Debug
deb.create()
