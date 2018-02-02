__author__ = 'RaldenProg'

import json
from timeit import default_timer as timer

import requests as req

from app.api.select_path import get_distance
from api.google.helpers.google_key import Google
from app.api.set_path import get_top_paths
from app.api.get_google_dist import get_google
from config import INDEXES


# It function normalize data about points (distance, user's priority, objective estimate)
# By MinMax Scaling method
# TODO: Try to make StandartScaling method of normalization
def normalize_point_data(distances, priority):
    for i in range(len(priority)):
        priority[i]/=5
    #print(priority)
    norm_priority = priority # 5 - max value of user's priorities
    result_matrix = []

    # Normalize data by distance
    for key_dist, dist in distances.items():
        matrix_row = []
        max_dist = max(dist, key=lambda x: x[1])[1]
        min_dist = min(dist, key=lambda x: x[1])[1]
        dist_diff = max_dist - min_dist

        max_estimate = max(dist, key=lambda x: x[3])[3] #
        min_estimate = min(dist, key=lambda x: x[3])[3] # TODO: Make in before cycle
        estimate_diff = max_estimate - min_estimate                  #

        for point in dist:
            # Change point's distance to it's normalized coefficient
            point_dist = 1 - (point[1] - min_dist)/dist_diff
            #print(point)
            # Change type of point to it's normalized estimation
            point_priority = norm_priority[point[2]]

            # Change objective estimate of point to it's normalized by local line estimate
            point_estimate = (point[3] - min_estimate)/estimate_diff

            # Result matrix's point forming
            norm_point = (point[0], point_dist + point_priority + point_estimate)

            matrix_row.append(norm_point)

        result_matrix.append(matrix_row)
    return result_matrix


def get_many(touch, max_time, priority):
    start = timer()
    google_key = Google.set_google_key()
    end = timer()
    print("google_key", end - start)

    graph, result_coord, id_list, time = get_distance(touch)

    #print("result_coord: ", result_coord)
    #print(graph)
    start = timer()
    touch_list = ""
    for i in id_list:
       touch_list += str(result_coord[i]['X']) + "," + str(result_coord[i]['Y']) + "%7C"
    #print(touch_list)
    touch0 = str(touch[0][0]) + ',' + str(touch[0][1])
    #print(touch0)

    end = timer()
    print("touch_list", end - start)
    count0_0 = 0
    count0_1 = 0
    start = timer()
    while(1):
        if count0_0 == 10:
            google_key = Google.set_google_key()
            count0_1 += 1
            if count0_1 == 20:
                return "Error"
        try:
            url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&mode=walking&origins={}&destinations={}&key={}".format(touch0, touch_list, google_key)
            answer0 = req.get(url)
            len_answer0 = len(json.loads(answer0.text)["rows"][0]["elements"])
            break
        except:
            count0_0 += 1

    #print(answer0.text)
    result0 = []
    for i in range(len_answer0):
        answ = json.loads(answer0.text)["rows"][0]["elements"][i]['duration']['text'].split()
        if len(answ) > 2:
            result0.append(int(answ[0]) * 60 + int(answ[2]))
        else:
            result0.append(int(answ[0]))

    end = timer()
    print("google_query_1", end - start)
    touch1 = str(touch[1][0]) + ',' + str(touch[1][1])

    start = timer()
    # print(touch1)
    while (1):
        if count0_0 == 10:
            google_key = set_google_key()
            count0_1 += 1
            if count0_1 == 20:
                return "Error"
        try:
            url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&mode=walking&origins={}&destinations={}&key={}".format(
            touch1, touch_list, google_key)
            answer1 = req.get(url)
            len_answer1 = len(json.loads(answer1.text)["rows"][0]["elements"])
            break
        except:
            count0_0 += 1

    #s.close()
    #print(answer1.text)
    result1 = []
    for i in range(len_answer1):
        answ = json.loads(answer1.text)["rows"][0]["elements"][i]['duration']['text'].split()
        if len(answ) > 2:
            result1.append(int(answ[0]) * 60 + int(answ[2]))
        else:
            result1.append(int(answ[0]))
    end = timer()
    print("google_query_2", end - start)
    N = len(graph) - 1
    for i in range(len(result0)):
        graph[0][i + 1] = result0[i]
        graph[i + 1][0] = result0[i]
        graph[N][i + 1] = result1[i]
        graph[i + 1][N] = result1[i]
    #pprint(graph)
    touch_get_google0 = str(touch[0][0]) + "," + str(touch[0][1])
    touch_get_google1 = str(touch[1][0]) + "," + str(touch[1][1])
    touch_google_list = [touch_get_google0, touch_get_google1]
    t = get_google(touch_google_list)
    graph[N][0] = t
    graph[0][N] = t
    new_graph = {}
    #print('graph  =  ', graph)
    for i in range(len(graph)):
        if i > 57 and i < 81:
            continue
        new_graph[i] = []
        for j in range(len(graph[i])):
            if j == 0:
                new_graph[i].append((j, graph[i][j], 0, 0))
            elif j == len(graph)-1:
                new_graph[i].append((j, graph[i][j], 0, 0))
            elif j > 0:
                if j > 57 and j < 81:
                    continue
                print(len(result_coord), j)
                tyobj = INDEXES.get(result_coord[j]['Type'], 0)
                #print(tyobj)
                try:
                    new_graph[i].append((j, graph[i][j], tyobj, result_coord[j]['Rating']))
                except:
                    pass
    print("new_graph", new_graph)
    print("prior: ", priority)
    coefficiet_graph = normalize_point_data(new_graph, priority)
    #print("!", coefficiet_graph)
    def new_element(l, element):
        new_l = list(l)
        new_l.append(element)
        return tuple(new_l)

    for i in range(len(coefficiet_graph)):
        for j in range(len(coefficiet_graph[i])):
            new_graph[i][j] = new_element(new_graph[i][j], coefficiet_graph[i][j][1])
        new_graph[i] = sorted(new_graph[i], key=lambda x: (x[1], x[4]))

    #print('START')
    #print(new_graph)
    result = get_top_paths(coefficiet_graph, time, max_time)
    #print("result_coord: ", result_coord)
    result = generate_answer(result, result_coord, id_list, N, touch)
    #return result0, result1, graph, time
    return result



def generate_answer(result, result_coord, id_list, N, touch_be):
    answer = {'route': []}
    #print("result: ", result)
    ch = 0
    for route in result:
        answer['route'].append({"name": [''], "time": [0], "descr": [None], "Y": [touch_be[0][1]], "type": [], "X": [touch_be[0][0]]})
        for touch in route['path']:
            if touch == 0 or touch == N:
                continue
            current_info = result_coord[id_list[touch-1]]
            #print(touch, "current_info: ", current_info)
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

#touch = ((55.05941, 82.912488), (55.030039, 82.920088))
#result = get_many(touch, 500)
#print(result)
touch = ((54.9870301969, 82.8739339379), (55.0666090889, 82.9952098502))
#result0, result1, graph, time = get_many(touch)
#result = get_many(touch, 100, [5, 3, 4, 2, 1])
#print(result)
#touch_get_google0 = str(touch[0][0]) + "," + str(touch[0][1])
#touch_get_google1 = str(touch[1][0]) + "," + str(touch[1][1])
#touch_google_list = [touch_get_google0, touch_get_google1]
#print(touch_google_list)
#print(graph)
#print('time')
#print(time)


#print('result')
#print(result)

