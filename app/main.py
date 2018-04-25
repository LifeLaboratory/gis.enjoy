# coding=utf-8
import flask
from flask_restful import Api
from route.route_list import ROUTES
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


if __name__ == '__main__':
    try:
        for route_class, route in ROUTES.items():
            api.add_resource(route_class, route)
        _app.run(host='0.0.0.0', port=13451, threaded=True)
    except Exception as e:
        print('Main except = ', e)
