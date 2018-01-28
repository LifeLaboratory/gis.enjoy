import requests as req
import json
from pprint import pprint
s = req.Session()

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
    print(answer.text)


test_geo()