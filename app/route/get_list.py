# coding=utf-8
from flask_restful import Resource
from api.helpers.service import Gis as gs

class List(Resource):
    def get(self):
        """
        parser = reqparse.RequestParser()
        parser.add_argument('data')
        args = parser.parse_args()
        print('GET /')
        print(request.headers)
        print('cookies = ', request.cookies)
        print('ARGS = ', args)
        data = args.get('data', None)
        print(data)
        data = json.loads(data)
        print(data["origin"])
        data_origin = []
        data_destination = []
        data_origin.append(float(data["origin"]["X"]))
        data_origin.append(float(data["origin"]['Y']))
        data_destination.append(float(data["destination"]["X"]))
        data_destination.append(float(data["destination"]["Y"]))
        data_origin = tuple(data_origin)
        data_destination = tuple(data_destination)
        #datas = (data_origin, data_destination)
        priority = []
        data_origin.append(float(data["priority"]))

        #print("datas", datas)
        #print("user_time", int(data["time"]))
        #answer = get_many(datas, int(data["time"]))
        #print("OK SEND")
        #answer = json.dumps(answer)
        """
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