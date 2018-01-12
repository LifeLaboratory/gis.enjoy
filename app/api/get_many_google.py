__author__ = 'RaldenProg'

from app.api.select_path import get_distance
from pprint import pprint
from app.google_key import KEY
import requests as req
import json
from app.api.set_path import get_top_paths
from app.api.get_google_dist import get_google


def get_many(touch, max_time):
    google_key = KEY()
    graph, result_coord, id_list, time = get_distance(touch)
    touch_list = ""
    for i in id_list:
       touch_list += str(result_coord[i]['X']) + "," + str(result_coord[i]['Y']) + "%7C"
    #print(touch_list)
    touch0 = str(touch[0][0]) + ',' + str(touch[0][1])
    #print(touch0)
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&mode=walking&origins={}&destinations={}&key={}".format(touch0, touch_list, google_key)
    #print(url)
    #s = req.Session()
    answer0 = req.get(url)
    #print(answer0.text)
    len_answer0 = len(json.loads(answer0.text)["rows"][0]["elements"])
    result0 = []
    for i in range(len_answer0):
        answ = json.loads(answer0.text)["rows"][0]["elements"][i]['duration']['text'].split()
        if len(answ) > 2:
            result0.append(int(answ[0]) * 60 + int(answ[2]))
        else:
            result0.append(int(answ[0]))

    touch1 = str(touch[1][0]) + ',' + str(touch[1][1])
    # print(touch1)
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&mode=walking&origins={}&destinations={}&key={}".format(
        touch1, touch_list, google_key)
    # print(url)

    answer1 = req.get(url)
    #s.close()
    #print(answer1.text)
    len_answer1 = len(json.loads(answer1.text)["rows"][0]["elements"])
    result1 = []
    for i in range(len_answer1):
        answ = json.loads(answer1.text)["rows"][0]["elements"][i]['duration']['text'].split()
        if len(answ) > 2:
            result1.append(int(answ[0]) * 60 + int(answ[2]))
        else:
            result1.append(int(answ[0]))
    N = len(graph) - 1
    for i in range(len(result0)):
        graph[0][i + 1] = result0[i]
        graph[i + 1][0] = result0[i]
        graph[N][i + 1] = result1[i]
        graph[i + 1][N] = result1[i]
    touch_get_google0 = str(touch[0][0]) + "," + str(touch[0][1])
    touch_get_google1 = str(touch[1][0]) + "," + str(touch[1][1])
    touch_google_list = [touch_get_google0, touch_get_google1]
    t = get_google(touch_google_list)
    graph[N][0] = t
    graph[0][N] = t
    result = get_top_paths(graph, time, max_time)
    result = generate_answer(result, result_coord, id_list, N, touch)

    #return result0, result1, graph, time
    return result


def generate_answer(result, result_coord, id_list, N, touch_be):
    answer = {'route': []}
    ch = 0
    for route in result:
        answer['route'].append({"name": [''], "time": [0], "descr": [None], "Y": [touch_be[0][1]], "type": [], "X": [touch_be[0][0]]})
        for touch in route['path']:
            if touch == 0 or touch == N:
                continue
            current_info = result_coord[id_list[touch-1]]
            answer['route'][ch]['name'].append(current_info['Name'])
            answer['route'][ch]['time'].append(current_info['Time'])
            answer['route'][ch]['descr'].append(current_info['Descr'])
            answer['route'][ch]['Y'].append(current_info['Y'])
            answer['route'][ch]['X'].append(current_info['X'])
            answer['route'][ch]['type'].append(current_info['Type'])
        answer['route'][ch]['name'].append('')
        answer['route'][ch]['time'].append(0)
        answer['route'][ch]['descr'].append(None)
        answer['route'][ch]['Y'].append(touch_be[1][1])
        answer['route'][ch]['X'].append(touch_be[1][0])
        answer['route'][ch]['type'].append('Touch')
        ch += 1
    return answer

touch = ((55.05941, 82.912488), (55.030039, 82.920088))
result = get_many(touch, 500)
print(result)
#touch = ((54.9870301969, 82.8739339379), (55.0666090889, 82.9952098502))
#result0, result1, graph, time = get_many(touch)
#result = get_many(touch)
#touch_get_google0 = str(touch[0][0]) + "," + str(touch[0][1])
#touch_get_google1 = str(touch[1][0]) + "," + str(touch[1][1])
#touch_google_list = [touch_get_google0, touch_get_google1]
#print(touch_google_list)
#print(graph)
#print('time')
#print(time)


#print('result')
#print(result)

