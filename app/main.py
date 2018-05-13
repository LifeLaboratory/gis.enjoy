# coding=utf-8
import sys
import os
sys.path.append(os.getcwd())
from flask import Flask, request
from flask_restful import Resource, Api
from route.route_geo import RouteGeo
from route.get_list import List
from route.route_filter import RouteFilter
_app = Flask(__name__)
_app.config['JSON_AS_ASCII'] = False
api = Api(_app)
HEADER = {'Access-Control-Allow-Origin': '*'}

# Выбор настройки
config = {
    'google': 'init_google',
    'nso': 'init_nso'
}


@_app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404


class Index(Resource):
    def get(self):
        print('GET /')
        print(request.headers)
        print('cookies = ', request.cookies)
        print('ARGS = ', request.args)
        return {'testing': 'testing'}, 200, HEADER


api.add_resource(Index, '/')
api.add_resource(RouteGeo, '/geo')
api.add_resource(List, '/list')
api.add_resource(RouteFilter, '/filter')

if __name__ == '__main__':
    try:
        _app.run(host='0.0.0.0', port=13451, threaded=True)
    except Exception as e:
        print('Main except = ', e)
