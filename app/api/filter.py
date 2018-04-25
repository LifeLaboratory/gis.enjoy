from api.helpers.service import Gis as gs

__author__ = 'RaldenProg'


class Filter:
    def __init__(self):
        self.__dict_type = {}
        self.__list_type = []

    def get_filter(self):
        get_sql = """
select distinct type
from geo
where type <> all('{"point_of_interest", "church", "park", "museum", "zoo", "funeral_home", "premise", "art_gallery"}'::text[])
"""
        dict_type = gs.SqlQuery(get_sql)
        result = []
        for d in dict_type:
            result.append(d["type"])
        return {"data": result}
