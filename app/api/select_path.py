import math
from api.helpers.service import Gis as gs

delta = 0.0005
#delta = 0.000000005

def select_avalible_points(start_point, finish_point):
    json_data_batch = []
    get_sql = ""
    result = ()
    dynamic_delta = 3*delta*math.sqrt(2)
    trying = 1

    while result is () and trying < 3:
        dynamic_delta = dynamic_delta * trying
        if start_point is not finish_point and trying == 1:
            if start_point[0] >= finish_point[0]:
                if start_point[1] >= finish_point[1]:
                    get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                        finish_point[0]-delta,
                        start_point[0]+delta,
                        finish_point[1]-delta,
                        start_point[1]+delta
                    )
                else:
                    get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                        finish_point[0] - delta,
                        start_point[0] + delta,
                        start_point[1] - delta,
                        finish_point[1] + delta
                    )
            else:
                if start_point[1] >= finish_point[1]:
                    get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                        start_point[0] - delta,
                        finish_point[0] + delta,
                        finish_point[1] - delta,
                        start_point[1] + delta
                    )
                else:
                    get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                        start_point[0] - delta,
                        finish_point[0] + delta,
                        start_point[1] - delta,
                        finish_point[1] + delta
                    )
        else:
            get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                start_point[0] + dynamic_delta,
                start_point[0] - dynamic_delta,
                start_point[1] + dynamic_delta,
                start_point[1] - dynamic_delta
            )
        #print(get_sql)
        get_sql = "SELECT * FROM Geo"
        result = gs.SqlQuery(get_sql)
        #print("SQLQUERY", result)
        #if result is not ():
            #for event in result:
                #json_data_batch.append(json.dumps(event))
        trying = trying + 1

    #print(json_data_batch)
    return result


def extract_coords(result_coord, time,  coord):
    """
    Метод извлекает из словаря ID координат и формирует словарь {id: {x: значение, Y: значение}}
    :param result_coord: ссылка на словарь содержащий id: координаты
    :param time: ссылка на список времени
    :param coord: словарь координат
    """
    temp_id = list()
    for touch in coord:
        id_coord = touch.get('id')
        time_coord = touch.get('time')
        temp_id.append(id_coord)
        time.append(time_coord)
        result_coord[id_coord] = {'X': touch.get('x'),
                                  'Y': touch.get('y'),
                                  'Descr': touch.get('descrip'),
                                  'Time': time_coord,
                                  'Type': touch.get('type'),
                                  'Name': touch.get('name'),
                                  'Rating': touch.get('rating')
                                  }
    time.append(0)
    #print(temp_id)
    return sorted(temp_id)


def genereate_pare(id_list):
    """
    Метод формирует кортеж всех пар координат
    :param id_list: список id координат
    """
    temp_coord = list()
    for i in range(len(id_list)):
        for j in range(i+1, len(id_list)):
            temp_coord.append((id_list[i], id_list[j]))
    return tuple(temp_coord)


def set_graph(graph, id_list, result, time):
    helper = dict()
    for i in range(len(id_list)):
        helper[id_list[i]] = i + 1
    for i in range(len(id_list) + 2):
        graph[i] = {i: 0}
    #pprint(helper)
    #print(graph)
    for pair in result:
        graph[helper[pair['point_1']]][helper[pair['point_2']]] = pair['distance']
        graph[helper[pair['point_2']]][helper[pair['point_1']]] = pair['distance']
    #print(graph)


def get_pair_distance():
    """
    Метод получает из базы дистанцию для всех пар значений координат
    :param coords: кортеж ID координат
    """
    get_sql = """
    with 
get_pair as (
select a.id as a_p, b.id as b_p from geo a, geo b where b.id <> a.id
),
get_coord as (
SELECT d.id, d.point_1, d.point_2, d.distance FROM geo_distance d, get_pair pair  WHERE (point_1, point_2) = (pair.a_p, pair.b_p) or (point_1, point_2) = (pair.b_p, pair.a_p)
)
select * from get_coord;
"""
    result = gs.SqlQuery(get_sql)
    #print(get_sql)
    # a = input()
    return result


def get_distance(touch):
    result_coord = dict()
    time = [0]
    coord = select_avalible_points(touch[0], touch[1])
    #print("coord", coord)
    id_list = extract_coords(result_coord, time, coord)
    #coords = genereate_pare(id_list)
    #print(id_list)
    #print("result coord", result_coord)

    result = get_pair_distance()#coords)
    N = len(id_list)+1
    graph = {0: {1:1, 2:4, 3:6, 4:10}, N: {}}
    set_graph(graph, id_list, result, time)

    #pprint(graph)

    return graph, result_coord, id_list, time

# p = select_avalible_points((55.028133392, 82.922988892),(55.028133391, 82.922988889))
# graph, result_coord, id_list, time = get_distance(((55.028133392, 82.922988892), (55.028133391, 82.922988889)))
# print(len(p))
# a = get_top_paths(graph, time, 500)
# print(a)
