from api.helpers.sql import Sql
import math

__author__ = 'ar.chusovitin'
delta = 0.0005


class Path:
    def __init__(self, start, finish, user_time):
        self.graph = {}
        self.distance = []
        self.coords = []
        self.dict_coords = {}
        self.id_list = []
        self.time = []
        self.start = start
        self.finish = finish
        self.user_time = user_time
        self.select_path()

    def select_path(self):
        self.coords = self.set_touch()
        self.id_list = self.get_coord()

    def set_touch(self):
        json_data_batch = []
        get_sql = ""
        result = ()
        dynamic_delta = 3*delta*math.sqrt(2)
        trying = 1
        while result is () and trying < 3:
            dynamic_delta = dynamic_delta * trying
            if self.start is not self.finish and trying == 1:
                if self.start[0] >= self.finish[0]:
                    if self.start[1] >= self.finish[1]:
                        get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                            self.finish[0] - delta,
                            self.start[0] + delta,
                            self.finish[1] - delta,
                            self.start[1] + delta
                        )
                    else:
                        get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                            self.finish[0] - delta,
                            self.start[0] + delta,
                            self.start[1] - delta,
                            self.finish[1] + delta
                        )
                else:
                    if self.start[1] >= self.finish[1]:
                        get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                            self.start[0] - delta,
                            self.finish[0] + delta,
                            self.finish[1] - delta,
                            self.start[1] + delta
                        )
                    else:
                        get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                            self.start[0] - delta,
                            self.finish[0] + delta,
                            self.start[1] - delta,
                            self.finish[1] + delta
                        )
            else:
                get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                    self.start[0] + dynamic_delta,
                    self.start[0] - dynamic_delta,
                    self.start[1] + dynamic_delta,
                    self.start[1] - dynamic_delta
                )
            # print(get_sql)
            get_sql = "SELECT * FROM Geo"
            result = Sql.exec(get_sql)
            trying = trying + 1
        return result

    def get_coord(self):
        temp_id = list()
        for touch in self.coords:
            id_coord = touch.get('id')
            time_coord = touch.get('time')
            temp_id.append(id_coord)
            self.time.append(time_coord)
            self.dict_coords[id_coord] = {'X': touch.get('x'),
                                          'Y': touch.get('y'),
                                          'Descr': touch.get('descrip'),
                                          'Time': time_coord,
                                          'Type': touch.get('type'),
                                          'Name': touch.get('name'),
                                          'Rating': touch.get('rating')
                                          }
        self.time.append(0)
        return sorted(temp_id)

    def get_touch(self):
        pass

    def set_distance(self):
        pass

    def set_graph(self):
        pass


