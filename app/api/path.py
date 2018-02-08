from api.helpers.sql import Sql
import math

__author__ = 'ar.chusovitin'
delta = 0.0005


class Path:
    def __init__(self, start, finish, user_time):
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
        self.select_path()

    def select_path(self):
        self.list_coords = self.set_touch()
        self.id_list = self.get_coord()

    def set_touch(self):
        get_sql = ""
        result = ()
        dynamic_delta = 3*delta*math.sqrt(2)
        trying = 1
        point = [0, 0, 0, 0]
        while result is () and trying < 3:
            dynamic_delta = dynamic_delta * trying
            if self.start is not self.finish and trying == 1:
                if self.start[0] >= self.finish[0]:
                    if self.start[1] >= self.finish[1]:
                        point[0] = self.finish[0] - delta
                        point[1] = self.start[0] + delta
                        point[2] = self.finish[1] - delta
                        point[3] = self.start[1] + delta
                    else:
                        point[0] = self.finish[0] - delta
                        point[1] = self.start[0] + delta
                        point[2] = self.start[1] - delta
                        point[3] = self.finish[1] + delta
                else:
                    if self.start[1] >= self.finish[1]:
                        point[0] = self.start[0] - delta
                        point[1] = self.finish[0] + delta
                        point[2] = self.finish[1] - delta
                        point[3] = self.start[1] + delta
                    else:
                        point[0] = self.start[0] - delta
                        point[1] = self.finish[0] + delta
                        point[2] = self.start[1] - delta
                        point[3] = self.finish[1] + delta
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
        result = Sql.exec(get_sql)
        return result

    def set_distance(self):
        pass

    def set_graph(self):
        pass


