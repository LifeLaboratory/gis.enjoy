# coding=utf-8
from flask_restful import Resource
from api.helpers.service import Gis as gs


class Test_route(Resource):

    def get(self):
        answer = gs.converter({
                    "route": [
                        {
                            "name": ["Lenina", "duck", "fuck", "ducken"],
                            "time": [20, 30, 40, 35],
                            "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
                            "Y": [56.845229, 56.839619, 56.840200, 56.841996],
                            "type": ["park", "galery", "park", "park"],
                            "X": [60.645281, 60.647116, 60.654428, 60.658903]
                        },
                        {
                            "name": ["Lenina", "duck", "ducken", "fuck"],
                            "time": [20, 30, 35, 40],
                            "descr": ["descr_lenina", "discr_duck", "duckduck", "discr_fuck"],
                            "Y": [56.845229, 56.839619, 56.841996, 56.840200],
                            "type": ["park", "galery", "park", "park"],
                            "X": [60.645281, 60.647116, 60.658903, 60.654428]
                        }
                    ]
                })
        return answer, 200, {'Access-Control-Allow-Origin': '*'}

    def options(self):
        return {'Allow': 'GET'}, 200, {'Access-Control-Allow-Origin': '*',
                                        'Access-Control-Allow-Methods': 'POST,GET',
                                        'Access-Control-Allow-Headers': 'Access-Control-Allow-Origin, '
                                                                        'Content-Type, '
                                                                        'X-Custom-Header'}