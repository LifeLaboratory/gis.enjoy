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
    SELECT * FROM filter
        """
        dict_type = Sql.exec(get_sql)
        result = dict()
        for filter_type in dict_type:
            result[filter_type['type']] = filter_type['id']
        return result
