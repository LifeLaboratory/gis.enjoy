import requests as req
import json
import app.api.set_path as sp
import app.api.select_path as select_p
from multiprocessing import Pool
from pprint import pprint
from app.google_key import KEY
from api.sql import SqlQuery
result = {}
list = []


def get_google(data):
    s = req.Session()
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&mode=walking&origins={}&destinations={}&key={}".format(data[0], data[1], KEY())

    #print(url)
    answer = s.get(url)
    #print(answer.text)
    answer = json.loads(answer.text)['rows'][0]['elements'][0]['duration']['text'].split()


    if len(answer) > 2:
        return int(answer[0])*60+int(answer[2])
    else:
        return int(answer[0])



def get_coords(touch, time=None):
    data = []
    json_batch = select_p.select_avalible_points(touch[0], touch[1])
    #print("jsn_b", len(json_batch))
    for i in range(len(json_batch)):
        buf = {}
        buf['x'] = json_batch[i]['x']
        buf['y'] = json_batch[i]['y']
        time.append(json_batch[i]['time'])
        data.append(buf)
    return data


def quer(touch, time=None):
    s = []
    data = get_coords(touch, time)
    #print(data)
    for i in range(len(data)):
        for j in range(len(data)):
            s.append((str(data[i]['x']) + ",%20" + str(data[i]['y']), str(data[j]['x']) + ",%20" + str(data[j]['y'])))
    with Pool(10) as p:
        list.extend(p.map(get_google, s))
    ch = 0
    for i in range(len(data)):
        result[i] = {}
        for j in range(len(data)):
            result[i][j] = list[ch]
            ch += 1
    return result, data


def set_route(result, data, id):
    for i in id:
        temp = {'name': [], 'X': [], 'Y': [], 'Time': [], 'Desc': [], 'Type': []}
        for j in i:
            temp['name'].append(data[j]['name'])
            temp['X'].append(data[j]['x'])
            temp['Y'].append(data[j]['y'])
            temp['Time'].append(data[j]['time'])
            temp['Desc'].append(data[j]['descript'])
            temp['Type'].append(data[j]['type'])
        result['route'].append(temp)


def get_finish(touch, user_time):
    time = []
    d, json_batch = quer(touch, time)
    #pprint(d)
    #pprint(json_batch)
    id = []
    names = {}
    #json_batch = select_p.select_avalible_points(touch[0], touch[1])

    for i in range(len(json_batch)):
        js = json_batch[i]
        #print(js)
        id_geo = js["Id"]
        names[id_geo] = js
        id.append(id_geo)
    sepa = sp.generate_roads(d, time, int(user_time))
    finish_id = []
    for i in range(len(sepa)):
        ids = []
        tuple_sepa = sepa[i]['path']
        list_sepa = [_ for _ in tuple_sepa]
        for j in range(len(list_sepa)):
            ids.append(id[list_sepa[j]])
        finish_id.append(ids)
    result = {'route': []}
    set_route(result, names, finish_id)
    return result


#if __name__ == '__main__':
#    touch = ((55.028133392, 82.922988892), (55.028133392, 82.922988892))
#    print(get_finish(touch, 600))


