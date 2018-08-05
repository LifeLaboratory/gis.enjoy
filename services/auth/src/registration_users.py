# coding=utf-8
import hashlib
import logging
import uuid
import api.base_name as names
from api.helpers.service import Gis as gs


def registration_user(user_data):
    """
    Метод проверяет корректность введенных данных
    :param user_data: dict данные пользователя
    :return: UUID сессии
    """
    check = [names.LOGIN, names.PASSWORD, names.NAME, names.EMAIL, names.SEX,
             names.CITY]
    registration_data = dict.fromkeys(check, '')
    error = False
    for data in check:
        if user_data.get(data, None) is None:
            logging.info('Incorrect parameter ' + data)
            registration_data[data] = 'Пустой параметр!'
            error = True
        else:
            registration_data[data] = user_data[data]
    if error:
        return {names.ANSWER: names.ERROR, names.DATA: registration_data}
    answer = input_auth_table(registration_data)
    if answer.get(names.ANSWER) is not names.SUCCESS:
        return {names.ANSWER: names.WARNING, names.DATA: {"error_info":"Ошибка запроса к базе данных"}}
    return answer


def input_auth_table(user_data):
    """
    Метод начинает цепочку регистрации в бд
    Заносится изменение в таблицу auth
    :param user_data: dict данные пользователя
    :return: UUID сессии
    """

    password_hash = hashlib.md5()
    password_hash.update(user_data[names.PASSWORD].encode())
    user_data[names.PASSWORD] = password_hash.hexdigest()
    sql = """INSERT INTO Auth_gis (login, password)
            VALUES ('{Login}','{Password}') RETURNING id_user""".format(
            Login=user_data.get(names.LOGIN),
            Password=user_data.get(names.PASSWORD))
    try:
        id_user = gs.SqlQuery(sql)[0]['id_user']
    except:
        logging.error('error: Ошибка запроса к базе данных. Возможно такой пользователь уже есть')
        return {names.ANSWER: names.WARNING,
                names.DATA: {"error_info":"Ошибка запроса к базе данных. Возможно такой пользователь уже есть"}}
    return input_user_table(id_user, user_data)


def input_user_table(id_user, user_data):
    """
    Промежуточный метод, добавляет данные в таблицу "Информация о пользователе"
    :param id_user: int ID пользователя
    :param user_data: dict Данные пользователя
    :return: UUID сессии
    """
    user_data[names.ID_USER] = id_user
    sql = """INSERT INTO Users_gis
             VALUES ({id_user},'{Name}','','{Email}',
            '{Sex}','{City}')"""\
        .format(**user_data)
    try:
        gs.SqlQuery(sql)
    except:
        logging.error('error: Ошибка запроса к базе данных')
        return {names.ANSWER: names.WARNING, names.DATA: {"error_info": "Ошибка запроса к базе данных"}}
    return input_session_table(id_user)


def input_session_table(id_user):
    """
    Конечный метод, регистрирует данные в таблицы "Сессии пользователей"
    :param id_user: int ID пользователя
    :return: UUID сессии
    """
    UUID = uuid.uuid4()
    sql = """INSERT INTO Session_gis (id_user, uuid)
            VALUES ({id}, '{UUID}')""".format(id=id_user, UUID=UUID)
    try:
        gs.SqlQuery(sql)
    except:
        logging.error('error: Ошибка запроса к базе данных')
        return {names.ANSWER: names.WARNING, names.DATA: {"error_info": "Ошибка запроса к базе данных"}}
    return {names.ANSWER: names.SUCCESS, names.DATA: {"UUID": str(UUID)}}
