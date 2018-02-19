# coding=utf-8
from flask_restful import Resource, reqparse
from api.filter import Filter

__author__ = 'RaldenProg'


class RouteFilter(Resource):
    def __init__(self):
        self.__filter = []
        self.__answer = []

    def get(self):
        self.__filter = Filter()
        self.__answer = self.__filter.get_filter()
        return self.__answer, 200, {'Access-Control-Allow-Origin': '*'}
