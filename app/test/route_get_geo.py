import requests as req
import json
s = req.Session()


def test_geo():
    data = {"origin": {
                        "X": 55.028133392,
                        "Y": 82.922988892
                    },
            "destination": {
                        "X": 55.028133392,
                        "Y": 82.922988892
                    }}
    url = "http://0.0.0.0:13451/geo?origin={}&destination={}".format(data["origin"], data["destination"])
    #print(url)
    answer = s.get(url)
    print(answer.text)


test_geo()