import requests as req
import json
s = req.Session()


def test_list():
    data =json.dumps({'Parks': [0, 1, 2, 3, 4]})
    answer = s.get("http://0.0.0.0:13451/list?dict={}".format(data))
    print(json.loads(answer.text))


test_list()