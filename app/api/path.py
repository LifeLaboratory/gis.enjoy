import math
from api.helpers.sql import Sql
from api.google.helpers.google import Google
__author__ = 'ar.chusovitin'
DELTA = 0.0005


class Path:
    def __init__(self, start, finish, user_time):
        self.google = Google((start, finish))
        self.dict_graph = {}
        self.list_distance = []
        self.list_coords = []
        self.dict_coords = {}
        self.id_list = []
        self.dict_pair_touch = {}
        self.list_time = []
        self.start = start
        self.finish = finish
        self.user_time = user_time
        self.new_graph = {}
        self.select_path()

    def select_path(self):
        self.list_coords = self.set_touch()
        self.id_list = self.get_coord()
        self.modif_graph()
        self.filtered_graph()
        #result = get_top_paths(coefficiet_graph, time, max_time)
        #result = generate_answer(result, result_coord, id_list, N, touch)

    def set_touch(self):
        get_sql = ""
        result = ()
        dynamic_delta = 3 * DELTA * math.sqrt(2)
        trying = 1
        point = [0, 0, 0, 0]
        while result is () and trying < 3:
            dynamic_delta = dynamic_delta * trying
            if self.start is not self.finish and trying == 1:
                if self.start[0] >= self.finish[0]:
                    if self.start[1] >= self.finish[1]:
                        point[0] = self.finish[0] - DELTA
                        point[1] = self.start[0] + DELTA
                        point[2] = self.finish[1] - DELTA
                        point[3] = self.start[1] + DELTA
                    else:
                        point[0] = self.finish[0] - DELTA
                        point[1] = self.start[0] + DELTA
                        point[2] = self.start[1] - DELTA
                        point[3] = self.finish[1] + DELTA
                else:
                    if self.start[1] >= self.finish[1]:
                        point[0] = self.start[0] - DELTA
                        point[1] = self.finish[0] + DELTA
                        point[2] = self.finish[1] - DELTA
                        point[3] = self.start[1] + DELTA
                    else:
                        point[0] = self.start[0] - DELTA
                        point[1] = self.finish[0] + DELTA
                        point[2] = self.start[1] - DELTA
                        point[3] = self.finish[1] + DELTA
            else:
                point[0] = self.start[0] + dynamic_delta
                point[1] = self.start[0] - dynamic_delta
                point[2] = self.start[1] + dynamic_delta
                point[3] = self.start[1] - dynamic_delta

            get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                point[0],
                point[1],
                point[2],
                point[3]
            )

            # print(get_sql)
            get_sql = "SELECT * FROM Geo"
            result = Sql.exec(get_sql)
            trying = trying + 1
        return result

    def get_coord(self):
        temp_id = list()
        for touch in self.list_coords:
            id_coord = touch.get('id')
            time_coord = touch.get('time')
            temp_id.append(id_coord)
            self.list_time.append(time_coord)
            self.dict_coords[id_coord] = {'X': touch.get('x'),
                                          'Y': touch.get('y'),
                                          'Descr': touch.get('descrip'),
                                          'Time': time_coord,
                                          'Type': touch.get('type'),
                                          'Name': touch.get('name'),
                                          'Rating': touch.get('rating')
                                         }
        self.list_time.append(0)
        return sorted(temp_id)

    def get_pair_touch(self):
        """
        Метод получает из базы дистанцию для всех пар значений координат
        :param coords: кортеж ID координат
        """
        get_sql = """
            with 
        get_pair as (
          select a.id as a_p, b.id as b_p 
          from geo a, geo b 
          where b.id <> a.id
        ),
        get_coord as (
          select d.id, d.point_1, d.point_2, d.distance 
          from geo_distance d, get_pair pair  
            where (point_1, point_2) = (pair.a_p, pair.b_p) 
            or (point_1, point_2) = (pair.b_p, pair.a_p)
        )
        select * from get_coord;
        """
        self.dict_pair_touch = Sql.exec(get_sql)

    def set_distance(self):
        pass

    def set_graph(self):
        helper = dict()
        for i in range(len(self.id_list)):
            helper[self.id_list[i]] = i + 1
        for i in range(len(self.id_list) + 2):
            self.dict_graph[i] = {i: 0}
        # pprint(helper)
        # print(graph)
        for pair in self.dict_pair_touch:
            self.dict_graph[helper[pair['point_1']]][helper[pair['point_2']]] = pair['distance']
            self.dict_graph[helper[pair['point_2']]][helper[pair['point_1']]] = pair['distance']
        # print(graph)

    def modif_graph(self):
        list_touch = self.google.get_one_to_many(self.list_coords)
        t = self.google.get_one_to_one(self.start, self.finish)
        N = len(self.dict_graph) - 1
        for i in range(len(list_touch)):
            self.dict_graph[0][i + 1] = list_touch[i]
            self.dict_graph[i + 1][0] = list_touch[i]
            self.dict_graph[N][i + 1] = list_touch[i]
            self.dict_graph[i + 1][N] = list_touch[i]
        self.dict_graph[N][0] = t
        self.dict_graph[0][N] = t

    def filtered_graph(self):


        # print('graph  =  ', graph)
        for i in range(len(self.dict_graph)):
            if i > 57 and i < 81:
                continue
            self.new_graph[i] = []
            for j in range(len(self.dict_graph[i])):
                if j == 0:
                    self.new_graph[i].append((j, self.dict_graph[i][j], 0, 0))
                elif j == len(self.dict_graph) - 1:
                    self.new_graph[i].append((j, self.dict_graph[i][j], 0, 0))
                elif j > 0:
                    if j > 57 and j < 81:
                        continue
                    #print(len(self.dict_coords), j)
                    #tyobj = INDEXES.get(self.dict_coords[j]['Type'], 0)
                    # print(tyobj)
                    try:
                        # new_graph[i].append((j, self.dict_graph[i][j], tyobj, self.dict_coords[j]['Rating']))
                        self.new_graph[i].append((j, self.dict_graph[i][j], self.dict_coords[j]['Rating']))
                    except:
                        pass

    def normalize_graph_coefficient(self):
        #coefficiet_graph = normalize_point_data(new_graph, priority)

        # print("!", coefficiet_graph)
        def new_element(l, element):
            new_l = list(l)
            new_l.append(element)
            return tuple(new_l)

        #for i in range(len(coefficiet_graph)):
        #    for j in range(len(coefficiet_graph[i])):
        #        self.new_graph[i][j] = new_element(self.new_graph[i][j], coefficiet_graph[i][j][1])
        #    self.new_graph[i] = sorted(self.new_graph[i], key=lambda x: (x[1], x[4]))

    def generate_answer(self, result, result_coord, id_list, N, touch_be):
        answer = {'route': []}
        # print("result: ", result)
        ch = 0
        for route in result:
            answer['route'].append(
                {"name": [''], "time": [0], "descr": [None], "Y": [touch_be[0][1]], "type": [], "X": [touch_be[0][0]]})
            for touch in route['path']:
                if touch == 0 or touch == N:
                    continue
                current_info = result_coord[id_list[touch - 1]]
                # print(touch, "current_info: ", current_info)
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
