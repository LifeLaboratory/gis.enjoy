from api.helpers.service import Gis as gs

__author__ = 'RaldenProg'


class Filter:
    def __init__(self):
        self.__dict_type = {}
        self.__list_type = []

    def get_filter(self):
        get_sql = "select distinct type FROM geo"
        dict_type = gs.SqlQuery(get_sql)
        result = []
        for d in dict_type:
            result.append(d["type"])
        return {"data": result}
