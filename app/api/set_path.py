import pprint
from operator import itemgetter


def generate_roads(graph, time=None, max_time=None):
    dist = {}
    pred = {}
    start = 0
    end = len(graph)-1
    for u in graph:
        dist[u] = {}
        pred[u] = {}
        for v in graph:
            dist[u][v] = None
            pred[u][v] = -1
        #pprint.pprint(dist)
    for u in graph:
        for neighbor in graph[u]:
            dist[u][neighbor] = graph[u][neighbor]
            pred[u][neighbor] = u
            dist[neighbor][u] = graph[u][neighbor]
        dist[u][u] = time[u]
    #pprint.pprint(dist)
    pos_start = 0
    pos_end = 1
    result = {(0,): 0}
    temp = [(0,)]
    #pprint.pprint(dist)
    res = list()
    #print(dist[4][5])
    for u in range(len(graph)):
        for v in range(len(graph)):
            #print('u = {} v = {} dist[u][v] = {}'.format(u, v, dist[u][v]))
            #print('TRUE')
            for i in range(pos_start, pos_end):
                index = list(temp[i])
                #print(index)
                pos = index[len(index)-1]
                #if index is [0, 2, 4]:
                #    print('index == ', index, v)
                #print(pos)
                #print(temp)
                #print(result)
                #print('IN >> temp[i] == {}  v = {}  pos = {}  result[temp[i]] == {}  dist[pos][v] == {}'.format(temp[i], v, pos,  result[temp[i]], dist[pos][v]))
                if v not in index and dist[pos][v]:
                    index.append(v)
                    #print(index)
                    #print(temp[i])
                    old_index = tuple(index)
                    temp.append(old_index)
                    #print('temp[i] == {}  v = {}  pos = {}  result[temp[i]] == {}  dist[pos][v] == {}'.format(temp[i], v, pos,  result[temp[i]], dist[pos][v]))
                    result[old_index] = result[temp[i]] + dist[pos][v] + dist[u][u]
                    if old_index[0] == start and old_index[len(old_index)-1] == end and result[old_index] <= max_time:
                        res.append({'path': old_index, 'point': result[old_index]})
        pos_start = pos_end
        pos_end = len(temp)
        #print(pos_start, pos_end)
    #pprint.pprint(result)
    #pprint.pprint(res)
    res = sorted(res, key=itemgetter('point'))
    return res

graph = {0: {1: 10, 2: 70, 5: 20},
         1: {2: 20, 3: 30, 4: 40},
         2: {3: 15, 4: 10},
         3: {4: 30, 5: 60},
         4: {5: 20},
         5: {}}
graph1 = {0: {0: 1, 1: 189, 2: 88, 3: 100, 4: 97},
         1: {0: 186, 1: 1, 2: 115, 3: 112, 4: 107},
         2: {0: 87, 1: 117, 2: 1, 3: 13, 4: 10},
         3: {0: 98, 1: 114, 2: 13, 3: 1, 4: 10},
         4: {0: 96, 1: 110, 2: 9, 3: 10, 4: 1}}
#time = [14, 15, 16, 17, 18]
#max_time = 240
#result = generate_roads(graph1, time, max_time)
#pprint.pprint(result)
