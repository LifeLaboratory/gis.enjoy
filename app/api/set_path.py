import pprint
from operator import itemgetter
from copy import deepcopy

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

top_paths = []
top_count = 5
# It's recursion function for top_count paths finding from begin_point to end_point
# and value of such paths less then max_time
def longest_paths(begin_point, end_point, current_point, graph, time, max_time, visited=None, current_path=None):
    global top_paths
    global top_count
    #print('len(top_paths) == ', len(top_paths))
    #print('top_paths == ', top_paths)
    #print('top_count == ', top_count)
    if len(top_paths) == top_count:
        return 1

    if begin_point == current_point:
        current_path = ([0], time[0])
        visited = [0] * (end_point + 1)
        #print(current_path, visited)

    if end_point == current_point:
        if current_path[1] <= max_time \
        and len(top_paths) < top_count \
        and current_path not in top_paths:
            top_paths.append({'path':current_path[0], 'point':current_path[1]})

        if len(top_paths) == top_count:
            return 1
        else:
            return 0

    visited[current_point] = 1
    for i in range(begin_point, end_point + 1):
        if graph[current_point][i][1] and visited[i] == 0:
            tmp = deepcopy(current_path)
            tmp[0].append(graph[current_point][i][0])
            tmp = (tmp[0], tmp[1] + graph[current_point][i][1] + time[i])
            if max_time < tmp[1]:
                return 0
            if tmp[1] + graph[current_point][i][1] <= max_time:
                if longest_paths(begin_point, end_point, graph[current_point][i][0], graph, time, max_time, visited, tmp) == 1:
                    return 1

    visited[current_point] = 0
    return 0


def get_top_paths(graph, time, max_time):
    global top_paths
    global top_count
    top_paths = []
    longest_paths(0, len(graph) - 1, 0, graph, time, max_time)
    return sorted(top_paths, key=itemgetter('point'))


graph = {0: {1: 10, 2: 70, 5: 20},
         1: {2: 20, 3: 30, 4: 40},
         2: {3: 15, 4: 10},
         3: {4: 30, 5: 60},
         4: {5: 20},
         5: {}}
graph1 = {0: {0: 0,   1: 186, 2: 87,  3: 98,  4: 96},
          1: {0: 186, 1: 0,   2: 117, 3: 114, 4: 110},
          2: {0: 87,  1: 117, 2: 0,   3: 13,  4: 9},
          3: {0: 98,  1: 114, 2: 13,  3: 0,   4: 10},
          4: {0: 96,  1: 110, 2: 9,   3: 10,  4: 0}}
time = [14, 15, 16, 17, 18]
max_time = 240
#result = generate_roads(graph1, time, max_time)
#pprint.pprint(result)

#res = get_top_paths(graph1, time, max_time)
#pprint.pprint(res)
