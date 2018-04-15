import api.base_name as names
import api.auth.auth as auth
from api.helpers.service import Gis as gs
from pprint import pprint

def validate_router(user_data):
    """
    Метод проверяет корректность параметров и если всё корректно, отправляет методу add_router
    :param user_data: dict хранит информацию о маршруте
    :return: router_id - идентификатор маршрута
    """
    check = [names.UUID, names.SCORE, names.NAME, names.ROUTE, names.IS_PRIVATE]
    user_info = dict.fromkeys(check, '')
    error = False
    for data in check:
        if user_data.get(data, None) is None:
            user_info[data] = 'Пустой параметр!'
            print("!", data)
            error = True
        else:
            user_info[data] = user_data[data]
    if error:
        return {names.ANSWER: names.WARNING, names.DATA: user_info}

    return add_router(user_info)


def add_router(user_data):
    """
    Метод проверяет пользователя и добавляет маршрут в базу
    :param user_data: dict хранит информацию о маршруте
    :return: router_id - идентификатор маршрута
    """
    user_data[names.ID_USER] = auth.session_verification(user_data[names.UUID])
    pprint(user_data)
    sql = """INSERT INTO routes_gis (id_user, is_private, score, name, route) VALUES
        ({id_user}, {is_private}, {score}, '{name}', '{route}') RETURNING id_route
        """.format(id_user=user_data[names.ID_USER],
                   is_private=user_data[names.IS_PRIVATE],
                   score=user_data[names.SCORE],
                   name=user_data[names.NAME],
                   route=gs.converter(user_data[names.ROUTE]))

    print(sql)
    try:
        result = gs.SqlQuery(sql)
        print(result)
    except:
        return {names.ANSWER: names.ERROR}
    if result is None:
        return {names.ANSWER: names.ERROR}
    return {names.ANSWER: names.SUCCESS, names.DATA: result[0]}



def get_router(param=None, data=None):
    if data is None:
        sql = """SELECT users_gis.name, routes_gis.id_route, routes_gis.route, routes_gis.name, routes_gis.score 
                FROM routes_gis INNER JOIN users_gis
                ON routes_gis.id_user = users_gis.id_user where routes_gis.is_private=false"""
        result = gs.SqlQuery(sql)
        return {names.ANSWER: names.SUCCESS, names.DATA: result}
    if param == "get_route":
        sql = """select route from routes_gis where id_route={}""".format(data["id_route"])
        result = gs.SqlQuery(sql)
        return {names.ANSWER: names.SUCCESS, names.DATA: result}
    if param == "get_usr":
        sql = "select route from routes_gis where id_user={}".format(data[names.ID])
        result = gs.SqlQuery(sql)
        return {names.ANSWER: names.SUCCESS, names.DATA: result}

