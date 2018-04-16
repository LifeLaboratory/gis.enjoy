# coding=utf-8
import math
from operator import itemgetter
from copy import deepcopy
from api.google.helpers.google import Google
from numpy import std
from api.helpers.service import Gis as gs
from api.Log import debug_write

DELTA = 0.05
top_paths = []
top_count = 5


class Path:
    def __init__(self, start, finish, user_time, user_filter, INDEXES):
        self.google = Google((start, finish))
        self.INDEXES = INDEXES
        self.user_filter = user_filter
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
        self.touches = None

    def select_path(self):
        self.list_coords = self.set_touch()

        self.id_list = self.get_coord()
        self.get_pair_touch()
        self.set_graph()


        self.new_graph = self.normalize_point_data(self.user_filter)
        result = self.get_top_paths(self.list_time, self.user_time)
        result = self.generate_answer(
            result, self.dict_coords,
            self.id_list,
            len(self.id_list) - 1,
            (self.start, self.finish)
        )
        debug_write(str(self.touches), str(result))
        return result

    def set_touch(self):
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
            result = gs.SqlQuery(get_sql)
            self.touches = result
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
        elements as (
          select unnest('{%s}'::integer[]) as id
        ),
        get_pair as (
          select b1.id as a_p, b2.id as b_p 
          from elements b1, elements b2
          where b1.id <> b2.id
        ),
        get_coord as (
          select d.id, d.point_1, d.point_2, d.distance 
          from geo_distance d, get_pair pair  
            where (point_1, point_2) = (pair.a_p, pair.b_p) 
            or (point_1, point_2) = (pair.b_p, pair.a_p)
        )
        select * from get_coord;
        """
        text = ''
        for i in self.id_list:
            text += '{}, '.format(i) if i != self.id_list[-1] else '{}'.format(i)

        #print(get_sql % (text))
        self.dict_pair_touch = gs.SqlQuery(get_sql % (text))

    def set_distance(self):
        pass

    def set_graph(self):

        '''
        Вспомогательный массив, который задаёт правило определения точки (достопримечательности)
        в матрице путей по её ID и наоборот
        '''
        helper = dict()
        for i in range(len(self.id_list)):
            helper[self.id_list[i]] = i + 1

        matrix_range = len(self.id_list) + 2
        self.dict_graph = [[[] for x in range(matrix_range)] for y in range(matrix_range)]
        '''
        Заполняем элементы матрицы путей - только достопримечательности
        Другими словами - кроме первых и последних столбцов и строк матрицы
        '''
        for pair in self.dict_pair_touch:
            i = helper[pair['point_1']]
            j = helper[pair['point_2']]
            try:
                tyobj = self.INDEXES.get(self.dict_coords[self.id_list[j-1]]['Type'], 0)
                self.dict_graph[i][j] = [j, pair['distance'], tyobj,
                                         self.dict_coords[self.id_list[j-1]]['Rating']]
            except:
                #print("{} {} tyobj Error 1".format(i,j))
                pass

            try:
                tyobj = self.INDEXES.get(self.dict_coords[self.id_list[i-1]]['Type'], 0)
                self.dict_graph[j][i] = [i, pair['distance'], tyobj,
                                         self.dict_coords[self.id_list[i-1]]['Rating']]
            except:
                #print("{} {} tyobj Error 2".format(j, i))
                pass
        '''
        Получение расстояния от начала и конца пути до всех выбранных достопримечательностей
        '''
        answer = self.google.get_fast(self.start, self.finish, self.list_coords)
        '''
        Заполнение первых и последних строк и столбцов матрицы
        '''
        N = len(self.dict_graph) - 1
        for i in range(len(answer['s']) - 1):
            try:
                tyobj = self.INDEXES.get(self.dict_coords[self.id_list[i]]['Type'], 0)
                self.dict_graph[N][i + 1] = [i + 1, answer['f'][i], tyobj,
                                             self.dict_coords[self.id_list[i]]['Rating']]
                self.dict_graph[0][i + 1] = [i + 1, answer['f'][i], tyobj,
                                             self.dict_coords[self.id_list[i]]['Rating']]
            except:
                #print("{} {} tyobj Error 3".format(N,i + 1))
                pass

            try:
                tyobj = self.INDEXES.get(self.dict_coords[self.id_list[i]]['Type'], 0)
                self.dict_graph[i + 1][N] = [N, answer['f'][i], tyobj,
                                             self.dict_coords[self.id_list[i]]['Rating']]
                self.dict_graph[i + 1][0] = [0, answer['f'][i], tyobj,
                                             self.dict_coords[self.id_list[i]]['Rating']]
            except:
                #print("{} {} tyobj Error 4".format(i + 1, N))
                pass

        self.dict_graph[N][0] = [0, answer['o'], 0, 0]
        self.dict_graph[0][N] = [N, answer['o'], 0, 0]
        self.dict_graph[0][0] = [0] * 4
        self.dict_graph[N][N] = [0] * 4

        '''
        Заполнение диагонали матрицы 
        '''
        for i in range(N):
            if i == 0:
                continue

            tyobj = self.INDEXES.get(self.dict_coords[self.id_list[i - 1]]['Type'], 0)
            self.dict_graph[i][i] = [i, 0, tyobj, self.dict_coords[self.id_list[i - 1]]['Rating']]

    def normalize_point_data(self, priority):
        """
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
        """

        result_matrix = []

        # Определение максимально приоритета
        max_priority = len(priority)

        sko_array = []
        #print("dict:", self.dict_graph[0])
        for element in self.dict_graph[0]:
            sko_array.append(element[1])

        sko = std(sko_array)

        try:
            time_per_priority = sko / len(self.dict_graph[0]) / max_priority # Соотношение количества времени к 1 условной единице приоритета
        except:
            time_per_priority = 0
        time_per_estimate = sko / len(self.dict_graph[0]) / 100 # Соотношение количества времени к 1 условной единице общей оценки

        for dist in self.dict_graph:
            matrix_row = []

            for point in dist:
                # Перевод приоритета во время
                try:
                    priority_to_time = (max_priority - priority.index(self.INDEXES.get(point[2], 0))) * time_per_priority
                except:
                    priority_to_time = 0
                #print(point)
                # Перевод оценки во время
                if point != []: # hot fix
                    estimate_to_time = point[3] * time_per_estimate

                    norm_point = (point[0], point[1], point[1] - priority_to_time - estimate_to_time)

                    matrix_row.append(norm_point)

            matrix_row = sorted(matrix_row, key=lambda x: x[2])
            result_matrix.append(matrix_row)
        return result_matrix

    def generate_answer(self, result, result_coord, id_list, N, touch_be):
        answer = {'route': []}
        ch = 0
        for route in result:
            answer['route'].append(
                {"name": [''], "time": [0], "descr": [None], "Y": [touch_be[0][1]], "type": [], "X": [touch_be[0][0]]})
            for touch in route['path']:
                if touch == 0 or touch == N + 2:
                    continue
                current_info = result_coord[id_list[touch - 1]]
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
            time, max_time, visited=None, current_path=None):
        '''
        Данный рекурсивный метод возвращает top_count маршрутов
        :param begin_point: Индекс начальной точки
        :param end_point: Индекс конечной точки
        :param current_point: Текущая точка
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
            visited = [0] * (end_point + 1)

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

        for i in range(begin_point, end_point + 1):
            if self.new_graph[current_point][i][1] \
                    and visited[self.new_graph[current_point][i][0]] == 0:
                tmp = deepcopy(current_path)
                tmp[0].append(self.new_graph[current_point][i][0])
                tmp = (tmp[0], tmp[1] + self.new_graph[current_point][i][1] + time[self.new_graph[current_point][i][0]])
                if max_time < tmp[1]:
                    return 0
                if tmp[1] <= max_time:
                    if self.longest_paths(
                            begin_point, end_point, self.new_graph[current_point][i][0],
                            time, max_time,
                            visited, tmp) == 1:
                        return 1
        visited[current_point] = 0
        return 0

    def get_top_paths(self, time, max_time):
        global top_paths
        global top_count
        top_paths = []
        self.longest_paths(0, len(self.new_graph) - 1, 0, time, max_time)
        return sorted(top_paths, key=itemgetter('point'), reverse=True)

