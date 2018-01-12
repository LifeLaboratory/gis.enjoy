from app.data.get_and_parse_data import db_connect
from pprint import pprint


def generate_distance_p2p():
    sql = "SELECT id, x, y FROM Geo"
    connect, current_connect = db_connect()
    current_connect.execute(sql)
    result = current_connect.fetchall()
    points = dict()
    for data in result:
        points[data.get('id')] = {'x': data.get('x'),
                                  'y': data.get('y')}
    key = sorted(points.keys())
    for i in range(len(key)):
        for j in range(i+1, len(key)):
            pass
            # тут делать запрос и добавлять в базу координаты в таблицу geo_distance


#generate_distance_p2p()
