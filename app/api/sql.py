import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE = {
    "dbname": "life_game_service",
    "user": "life_dev",
    "host": "90.189.132.25",
    "password": "PINLOX!@#"
}


def db_connect():
    try:
        connect = psycopg2.connect("dbname='{dbname}' user='{user}' host='{host}' password='{password}'".format(**DATABASE))
        return connect, connect.cursor(cursor_factory=RealDictCursor)
    except:
        raise


def SqlQuery(query):
    """
    Метод выполняет SQL запрос к базе
    :param query: str SQL запрос
    :return: dict результат выполнения запроса
    """
    connect, current_connect = db_connect()
    result = None
    try:
        #print(query)
        current_connect.execute(query)
        connect.commit()
    except:
        return result
    finally:
        try:
            result = current_connect.fetchall()
        except:
            return result
        connect.close()
        return result