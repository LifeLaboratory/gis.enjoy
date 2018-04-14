from api.helpers.service import Gis as gs

__author__ = 'RaldenProg'


class Filter:
    def __init__(self):
        self.__dict_type = {}
        self.__list_type = []

    def get_filter(self):
        get_sql = """select distinct type FROM geo where type!='point_of_interest' and type!='church' and type !='park' and
                type!='museum' and type!='zoo' and type!='funeral_home' and type!='premise' and type!='art_gallery'
                """
        dict_type = gs.SqlQuery(get_sql)
        result = []
        for d in dict_type:
            result.append(d["type"])
        return {"data": result}
