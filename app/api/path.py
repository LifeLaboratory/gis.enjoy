import math

from operator import itemgetter
from copy import deepcopy
from api.helpers.sql import Sql
from api.google.helpers.google import Google
from api.filter import Filter
import time
__author__ = 'ar.chusovitin'
DELTA = 0.0005

top_paths = []
top_count = 5


class Path:
    def __init__(self, start, finish, user_time):
        self.google = Google((start, finish))
        self.INDEXES = Filter().get_filter()
        self.dict_graph = {}
        self.list_distance = []
        self.list_coords = []
        self.dict_coords = {}
        self.id_list = []
        self.dict_pair_touch = {}
        self.list_time = [0]
        self.start = start
        self.finish = finish
        self.user_time = user_time
        self.new_graph = {}
        self.result = self.select_path()

    def select_path(self):
        start = time.time()
        self.list_coords = self.set_touch()
        print('set_touch = ', time.time() - start)

        start = time.time()
        self.id_list = self.get_coord()

        print('get_coord = ', time.time() - start)
        start = time.time()
        self.get_pair_touch()

        print('get_pair_touch = ', time.time() - start)
        start = time.time()
        self.set_graph()

        print('set_graph = ', time.time() - start)
        start = time.time()
        self.modif_graph()

        print('modif_graph = ', time.time() - start)
        a = 1
        self.filtered_graph()
        # Не могу понять откуда брать массив со списком приоритетов от пользователя
        # Поэтому вставил свой кастомный массив
        self.new_graph = self.normalize_point_data(["Парк", "Музей"])
        result = self.get_top_paths(self.new_graph, self.list_time, self.user_time)
        result = self.generate_answer(
            result, self.dict_coords,
            self.id_list,
            len(self.id_list) - 1,
            (self.start, self.finish)
        )
        return result

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

            get_sql = "SELECT * FROM Geo"
            result = Sql.exec(get_sql)
            trying = trying + 1
        return result

    def get_coord(self):
        temp_id = []
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
        a =1
        for pair in self.dict_pair_touch:
            self.dict_graph[helper[pair['point_1']]][helper[pair['point_2']]] = pair['distance']
            self.dict_graph[helper[pair['point_2']]][helper[pair['point_1']]] = pair['distance']
        # print(graph)

    def modif_graph(self):

        start = time.time()
        answer = self.google.get_fast(self.start, self.finish, self.list_coords)
        '''
        list_touch_start_to_all = self.google.get_one_to_many(self.start, self.list_coords)
        print('start = ', time.time() - start)
        start = time.time()
        list_touch_finish_to_all = self.google.get_one_to_many(self.finish, self.list_coords)
        print('finish = ', time.time() - start)
        start = time.time()
        t = self.google.get_one_to_one(self.start, self.finish)
        '''
        print('one_to_one = ', time.time() - start)
        N = len(self.dict_graph) - 1
        for i in range(len(answer['s'])):
            self.dict_graph[0][i + 1] = answer['s'][i]
            self.dict_graph[i + 1][0] = answer['s'][i]
            self.dict_graph[N][i + 1] = answer['f'][i]
            self.dict_graph[i + 1][N] = answer['f'][i]
        self.dict_graph[N][0] = answer['o']
        self.dict_graph[0][N] = answer['o']

    def filtered_graph(self):
        for i in self.dict_graph:
            self.new_graph[i] = []
            for j in self.dict_graph[i]:
                if j == 0:
                    self.new_graph[i].append((j, self.dict_graph[i][j], 0, 0))
                elif j == len(self.dict_graph[i]) - 1:
                    self.new_graph[i].append((j, self.dict_graph[i][j], 0, 0))
                elif 0 < j < len(self.dict_graph[i]):
                    # print(len(self.dict_coords), j)
                    tyobj = self.INDEXES.get(self.dict_coords[self.id_list[j - 1]]['Type'], 0)
                    # print(tyobj)
                    try:
                        self.new_graph[i].append((j, self.dict_graph[i][j], tyobj, self.dict_coords[self.id_list[j]]['Rating']))
                        #self.new_graph[i].append((j, self.dict_graph[i][j], self.dict_coords[j]['Rating']))
                    except:
                        pass

    def normalize_point_data(self, priority):
        '''
        Данный метод приводит 4 параметра, характеризующих точку матрицы @distances
        (номер точки, время до точки, тип точки, общая оценка точки),к одной единице измерения - времени.
        Другими словами, определяет какое приемлемое количество времени пользователь
        готов потратить, чтобы перейти к более приоритетному типу достопримечательности,
        или к месту, с более высокой общей оценкой.

        :param priority: Интексы типы выбранных достопримечательностей (из INDEXES), с учётом приоритета
        пользователя
        :return: Матрица взвешанных путей между точками, отсортированная по убыванию
        взвешанных весов, где каждый элемент представлен в виде кортежа
        (номер точки, время до точки, нормализованное время до точки)
        '''

        result_matrix = []

        # Определение максимально приоритета
        max_priority = len(priority)

        summ = 0
        for element in self.new_graph[0]:
            summ += element[1]

        time_per_priority = summ / len(self.new_graph[0]) / max_priority # Соотношение количества времени к 1 условной единице приоритета
        time_per_estimate = summ / len(self.new_graph[0]) / 100 # Соотношение количества времени к 1 условной единице общей оценки

        for key_dist, dist in self.new_graph.items():
            matrix_row = []

            for point in dist:
                # Перевод приоритета во время
                try:
                    priority_to_time = (max_priority - priority.index(self.INDEXES.get(point[2], 0))) * time_per_priority
                except:
                    priority_to_time = 0

                # Перевод оценки во время
                estimate_to_time = point[3] * time_per_estimate

                norm_point = (point[0], point[1], point[1] - priority_to_time - estimate_to_time)

                matrix_row.append(norm_point)

            matrix_row = sorted(matrix_row, key=lambda x: x[2])
            result_matrix.append(matrix_row)
        return result_matrix

    def normalize_graph_coefficient(self):
        coefficiet_graph = self.normalize_point_data(["Парк", "Музей"])

        # print("!", coefficiet_graph)
        def new_element(l, element):
            new_l = list(l)
            new_l.append(element)
            return tuple(new_l)

        for i in range(len(coefficiet_graph)):
            for j in range(len(coefficiet_graph[i])):
                self.new_graph[i][j] = new_element(self.new_graph[i][j], coefficiet_graph[i][j][1])
            self.new_graph[i] = sorted(self.new_graph[i], key=lambda x: (x[1], x[4]))

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

    def generate_roads(self, graph, time=None, max_time=None):
        dist = {}
        pred = {}
        start = 0
        end = len(graph) - 1
        for u in graph:
            dist[u] = {}
            pred[u] = {}
            for v in graph:
                dist[u][v] = None
                pred[u][v] = -1
        for u in graph:
            for neighbor in graph[u]:
                dist[u][neighbor] = graph[u][neighbor]
                pred[u][neighbor] = u
                dist[neighbor][u] = graph[u][neighbor]
            dist[u][u] = time[u]
        pos_start = 0
        pos_end = 1
        result = {(0,): 0}
        temp = [(0,)]
        res = list()
        for u in range(len(graph)):
            for v in range(len(graph)):
                for i in range(pos_start, pos_end):
                    index = list(temp[i])
                    pos = index[len(index) - 1]
                    if v not in index and dist[pos][v]:
                        index.append(v)
                        old_index = tuple(index)
                        temp.append(old_index)
                        result[old_index] = result[temp[i]] + dist[pos][v] + dist[u][u]
                        if old_index[0] == start \
                                and old_index[len(old_index) - 1] == end \
                                and result[old_index] <= max_time:
                            res.append({'path': old_index, 'point': result[old_index]})
            pos_start = pos_end
            pos_end = len(temp)
        res = sorted(res, key=itemgetter('point'))
        return res


    def longest_paths(
            self, begin_point, end_point, current_point,
            graph, time, max_time, visited=None, current_path=None):
        '''
        Данный рекурсивный метод возвращает top_count маршрутов
        :param begin_point: Индекс начальной точки
        :param end_point: Индекс конечной точки
        :param current_point: Текущая точка
        :param graph: Матрица точек, каждый элемент которой представлен
        в виде кортежа (индекс точки, предобработанное время до точки)
        :param time: Массив времён, которое пользователь может провести на
        каждом из мест
        :param max_time: Максимальное время, которое есть у пользователя в
        распоряжении
        :param visited: Массив уже посещённых точек
        :param current_path: Массив из точек, которые представляют собой
        маршрут
        :return: top_paths - массив из top_count маршрутов
        '''
        global top_paths
        global top_count
        if len(top_paths) == top_count:
            return 1

        if begin_point == current_point:
            current_path = ([0], time[0])
            visited = [0] * (end_point)

        if end_point == current_point:
            if current_path[1] <= max_time \
                    and len(top_paths) < top_count \
                    and current_path not in top_paths:
                top_paths.append({'path': current_path[0], 'point': current_path[1]})

            if len(top_paths) == top_count:
                return 1
            else:
                return 0

        visited[current_point] = 1

        for i in range(begin_point, end_point):
            if i == 20:
                a = 1
            if graph[current_point][i][1] and visited[graph[current_point][i][0]] == 0:
                tmp = deepcopy(current_path)
                tmp[0].append(graph[current_point][i][0])
                tmp = (tmp[0], tmp[1] + graph[current_point][i][1] + time[graph[current_point][i][0]])
                if max_time < tmp[1]:
                    return 0
                if tmp[1] <= max_time:
                    if self.longest_paths(
                            begin_point, end_point, graph[current_point][i][0],
                            graph, time, max_time,
                            visited, tmp) == 1:
                        return 1

        visited[current_point] = 0
        return 0

    def get_top_paths(self, graph, time, max_time):
        global top_paths
        global top_count
        top_paths = []
        self.longest_paths(0, len(graph) - 1, 0, graph, time, max_time)
        return sorted(top_paths, key=itemgetter('point'))


if __name__ == '__main__':
    start = time.time()
    print('Start')

    print(Path((56.8362039, 60.617562), (56.8362039, 60.617562), 1000).result)
    print(time.time() - start)
