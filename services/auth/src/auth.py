# coding=utf-8
from api.auth.registration_users import *
from api.helpers.service import Gis as gs


def session_verification(session):
    """
    Метод проверяет, существует ли пользовательская сессия
    :param session: UUID сессии
    :return: int Возвращает ID пользователя
    """
    try:
        sql = "SELECT id_user FROM Session_gis WHERE UUID = '{}'".format(session)
        result = gs.SqlQuery(sql)
    except:
        return None
    try:
        if len(result) == 0:
            return None
    except:
        return None
    return result[0]["id_user"]


def get_login(id_user):
    """
    Метод получает логин по ID пользователя
    :param id_user: ID пользователя
    :return: str Логин пользователя
    """
    try:
        sql = "SELECT Login FROM Auth_gis WHERE User = '{}'".format(id_user)
        result = gs.SqlQuery(sql)
    except:
        return None
    try:
        if len(result) == 0:
            return None
    except:
        return None
    return result[names.LOGIN]


def get_user_name(id_user):
    """
    Метод возвращает имя пользователя
    :param id_user: int, id пользователя
    :return:
    """
    sql = """Select name from users_gis where id_user = {id_user}""".format(id_user=id_user)
    try:
        result = gs.SqlQuery(sql)
    except:
        return {names.ANSWER: names.ERROR}
    return {names.ANSWER: names.SUCCESS, names.DATA: result[0]}


def login_verification(user_data):
    """
    Метод проверяет корректность параметров и если всё корректно, передает в метод auth_user
    :param user_data: dict хранит информацию о пользователе
    :return: UUID сессии
    """
    check = [names.LOGIN, names.PASSWORD]
    user_info = dict.fromkeys(check, '')
    error = False
    for data in check:
        if user_data.get(data, None) is None:
            user_info[data] = 'Пустой параметр!'
            error = True
        else:
            user_info[data] = user_data[data]
    if error:
        return {names.ANSWER: names.WARNING, names.DATA: {"user_info": user_info}}
    return auth_user(user_info)


def auth_user(user_data):
    """
    Метод авторизирует пользователя, присваивая ему UUID сессии
    :param user_data: dict хранит информацию о пользователе
    :return: UUID сессии
    """
    password_hash = hashlib.md5()
    password_hash.update(user_data[names.PASSWORD].encode())
    user_data[names.PASSWORD] = password_hash.hexdigest()
    try:
        sql = "SELECT id_user FROM Auth_gis WHERE Login = '{}' and Password = '{}'".format(user_data[names.LOGIN],
                                                                                           user_data[names.PASSWORD])
        result = gs.SqlQuery(sql)
    except:
        return {names.ANSWER: "Ошибка запроса к базе данных"}
    try:
        if len(result) == 0:
            return {names.ANSWER: names.WARNING, names.DATA: {"error_info":"Данного пользователя нет в базе данных"}}
    except:
        return {names.ANSWER: names.WARNING, names.DATA: {"error_info":"Логин или пароль не правильные"}}
    answer = input_session_table(result[0].get(names.ID_USER))
    if answer.get(names.ANSWER) is not names.SUCCESS:
        return {names.ANSWER: names.WARNING, names.DATA: {"error_info":"Ошибка запроса к базе данных. Неудача"}}
    return answer


def logout_user(session):
    """
    Метод закрывает сессию пользователя
    :param session: UUID сессии, которую нужно закрыть
    """
    try:
        sql = "DELETE FROM Session_gis WHERE UUID = '{}'".format(session)
        result = gs.SqlQuery(sql)
    except:
        return {names.ANSWER: "Ошибка запроса к базе данных"}
    try:
        if len(result) == 0:
            return {names.ANSWER: names.WARNING, names.DATA: {"error_info":"Такой сессии нет в базе"}}
    except:
        return {names.ANSWER: names.WARNING, names.DATA: {"error_info": "Сессия неверная"}}
