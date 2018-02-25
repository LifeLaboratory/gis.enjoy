# coding=utf-8
from flask_restful import Resource
from api.filter import Filter

__author__ = 'RaldenProg'


class RouteFilter(Resource):
    def __init__(self):
        self.__filter = Filter()

    def get(self):
        answer = self.__filter.get_filter()
        return answer, 200, {'Access-Control-Allow-Origin': '*'}
