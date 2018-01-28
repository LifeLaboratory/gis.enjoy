from api.sql import SqlQuery

def generate_distance_p2p():
    sql = "SELECT id, x, y FROM Geo"
    result = SqlQuery(sql)
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
