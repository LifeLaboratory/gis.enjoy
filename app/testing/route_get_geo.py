import requests as req
import json
from time import time
from pprint import pprint
from multiprocessing import Process
s = req.Session()


def test_route():
    start = time()
    data = s.get('http://127.0.0.1:13451/geo?data={"origin":{"X":55.750683047374665,"Y":37.61085501586922},"destination":{"X":55.75353294349821,"Y":37.601241978759845},"time":480,"priority":["Памятник","Театр"]}')
    end = time()
    print('start = {}\nend = {}\nend-start = {} '.format(start, end, end - start))
    print(data.text)


def test_geo():
    data = json.dumps({"origin": {
                        "X": 55.028133392,
                        "Y": 82.922988892
                    },
            "destination": {
                        "X": 55.028133391,
                        "Y": 82.922988889
                    },
            "time": 5
    })
    #print(data)
    url = "http://0.0.0.0:13451/geo?data={}".format(data)
    #pprint(url)
    answer = s.get(url)
    #print(answer.text)


if __name__ == '__main__':
    start = time()
    p = None
    for i in range(15):
        p = Process(target=test_route)
        p.start()
    p.join()
    print('time end: ', time() - start)