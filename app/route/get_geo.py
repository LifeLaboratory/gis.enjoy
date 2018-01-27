# coding=utf-8
from flask_restful import Resource, reqparse
from flask import request
from app.api.config import HEADER
import json
from ast import literal_eval
from app.api.get_many_google import get_many
from pprint import pprint
from api.config import INDEXES
from api.sql import converter
class Geo(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data')
        args = parser.parse_args()
        #print('GET /')
        #print(request.headers)
        #print('cookies = ', request.cookies)
        #print('ARGS = ', args)
        data = args.get('data', None)

        data = converter(data)
        #print(data)
        #print(data["origin"])
        data_origin = []
        data_destination = []
        data_origin.append(float(data["origin"]["X"]))
        data_origin.append(float(data["origin"]['Y']))
        data_destination.append(float(data["destination"]["X"]))
        data_destination.append(float(data["destination"]["Y"]))
        data_origin = tuple(data_origin)
        data_destination = tuple(data_destination)
        datas = (data_origin, data_destination)
        priority = []
        index_priority = []
        for i in range(len(data["priority"])):
            for j in range(len(INDEXES)):
                if data["priority"][i] == INDEXES[j]:
                    index_priority.append(5-j)
        print("index_priority", index_priority)
        print("datas", datas)
        #print("user_time", int(data["time"]))
        answer = get_many(datas, int(data["time"]), index_priority)
        #print(answer)
        #answer = 1
        #answer = json.dumps(answer)
        return answer, 200, {'Access-Control-Allow-Origin': '*'}

    def options(self):
        return {'Allow': 'GET'}, 200, {'Access-Control-Allow-Origin': '*',
                                        'Access-Control-Allow-Methods': 'POST,GET',
                                        'Access-Control-Allow-Headers': 'Access-Control-Allow-Origin, '
                                                                        'Content-Type, '
                                                                        'X-Custom-Header'}
