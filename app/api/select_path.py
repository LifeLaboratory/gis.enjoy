
from app.data.get_and_parse_data import db_connect
import math
import json

delta = 0.000005

def select_avalible_points(start_point, finish_point):
    json_data_batch = []
    connect, current_connect = db_connect()
    if connect == -1:
        return {"Answer": "Warning", "Data": "Ошибка доступа к базе данных, повторить позже"}
    get_sql = ""
    result = ()
    dynamic_delta = 3*delta*math.sqrt(2)
    trying = 1

    while result is () and trying < 3:
        dynamic_delta = dynamic_delta * trying
        if start_point is not finish_point and trying == 1:
            if start_point[0] >= finish_point[0]:
                if start_point[1] >= finish_point[1]:
                    get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                        finish_point[0]-delta,
                        start_point[0]+delta,
                        finish_point[1]-delta,
                        start_point[1]+delta
                    )
                else:
                    get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                        finish_point[0] - delta,
                        start_point[0] + delta,
                        start_point[1] - delta,
                        finish_point[1] + delta
                    )
            else:
                if start_point[1] >= finish_point[1]:
                    get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                        start_point[0] - delta,
                        finish_point[0] + delta,
                        finish_point[1] - delta,
                        start_point[1] + delta
                    )
                else:
                    get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                        start_point[0] - delta,
                        finish_point[0] + delta,
                        start_point[1] - delta,
                        finish_point[1] + delta
                    )
        else:
            get_sql = "SELECT * FROM Geo WHERE x >= {} and x <= {} and y >= {} and y <= {}".format(
                start_point[0] + dynamic_delta,
                start_point[0] - dynamic_delta,
                start_point[1] + dynamic_delta,
                start_point[1] - dynamic_delta
            )

        current_connect.execute(get_sql)
        result = current_connect.fetchall()
        if result is not ():
            for event in result:
                json_data_batch.append(json.dumps(event))
        trying = trying + 1

    #print(json_data_batch)
    return json_data_batch

#select_avalible_points((55.028133392, 82.922988892),(55.028133391, 82.922988889))
