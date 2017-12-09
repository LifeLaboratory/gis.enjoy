import requests as req
import json
s = req.Session()


def test_geo():
    data = {'param': 'Parks',
            'page': 1}
    answer = s.get("http://0.0.0.0:13451/geo?param={}&page={}".format(data['param'], data['page']))
    print(answer.text)


test_geo()