from api.helpers.sql import Sql

__author__ = 'RaldenProg'


class Filter:
    def __init__(self):
        self.__dict_type = {}
        self.__list_type = []

    def get_filter(self):
        get_sql = """
            with
            filter as (
    SELECT DISTINCT id, type FROM geo
    )
    SELECT type FROM filter
        """
        dict_type = Sql.exec(get_sql)
        result = []
        for d in dict_type:
            result.append(d["type"])
        return {"data": result}
