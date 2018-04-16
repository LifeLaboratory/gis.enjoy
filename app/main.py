# coding=utf-8
import flask
from flask_restful import Resource, Api

from route.Authentication import Authentication
from route.Logout import Logout
from route.Registration import Registration
from route.Routes import Route
from route.get_list import List
from route.route_debug import Debug
from route.route_filter import RouteFilter
from route.route_geo import RouteGeo

from api.Log import Log

_app = flask.Flask(__name__)
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
        return {'testing': 'testing'}, 200, HEADER


api.add_resource(Index, '/')
api.add_resource(RouteGeo, '/geo')
api.add_resource(List, '/list')
api.add_resource(RouteFilter, '/filter')
api.add_resource(Authentication, '/auth')
api.add_resource(Registration, '/registration')
api.add_resource(Debug, '/debug')
api.add_resource(Logout, '/logout')
api.add_resource(Route, '/route')

if __name__ == '__main__':
    try:
        _app.run(host='0.0.0.0', port=13451, threaded=True)
    except Exception as e:
        print('Main except = ', e)
