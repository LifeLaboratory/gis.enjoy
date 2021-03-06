import logging
from datetime import datetime
import os
import api.base_name as names

__author__ = 'RaldenProg'


class Log:
    logging.basicConfig(filename='logger.log',
                        format='%(filename)-12s[LINE:%(lineno)d] %(levelname)-8s %(message)s %(asctime)s ',
                        level=logging.DEBUG)


def debug_write(graph, result):
    os.getcwd()
    date_now = datetime.now().strftime('%Y.%m.%d:%H.%M.%S')
    directory = "Debug_files/" + date_now.split(":")[0] + "/" + date_now
    if not os.path.exists("Debug_files"):
        os.mkdir("Debug_files")
    if not os.path.exists("Debug_files/" + date_now.split(":")[0]):
        os.mkdir("Debug_files/" + date_now.split(":")[0])
    if not os.path.exists("Debug_files/" + date_now.split(":")[0] + "/" + date_now):
        os.mkdir(directory)
    f = open(directory + '/graph.txt', 'w')
    f.write(graph)
    f.close()
    f = open(directory + '/result.txt', 'w')
    f.write(result)
    f.close()


def debug_read(arg=None, dir=None):
    os.chdir("Debug_files")
    if arg is None:
        answer = os.listdir()
        os.chdir("..")
        return {names.ANSWER: names.SUCCESS, names.DATA: answer}
    if arg == '1' and dir is not None:
        os.chdir(dir)
        answer = os.listdir()
        os.chdir("..")
        os.chdir("..")
        return {names.ANSWER: names.SUCCESS, names.DATA: answer}
    if arg == '2' and dir is not None:
        os.chdir(dir.split(":")[0])
        os.chdir(dir)
        f = open('result.txt')
        result = f.read()
        f.close()
        f = open('graph.txt')
        graph = f.read()
        f.close()
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        return {names.ANSWER: names.SUCCESS, names.DATA: {"graph": graph, "result": result}}
