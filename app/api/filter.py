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
    SELECT DISTINCT type FROM geo
    )
    SELECT * FROM filter
        """
        self.dict_type = Sql.exec(get_sql)
        for i in self.dict_type:
            self.__list_type.append(i['type'])
        return self.__list_type
