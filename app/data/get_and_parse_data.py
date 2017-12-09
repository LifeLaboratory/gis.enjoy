# encoding: utf-8
import csv
import json
import requests as req
import pymysql
import wget
import re

url_gov = "http://maps.nso.ru/232/getcsv.php?file=%D0%9E%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D1%8B%20%D0%BA%D1%83%D0%BB%D1%8C%D1%82%D1%83%D1%80%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%BD%D0%B0%D1%81%D0%BB%D0%B5%D0%B4%D0%B8%D1%8F.csv"
gov_file_name = "gov_dataset.csv"

def get_csv(url):
    try:
        file = open(gov_file_name)
    except Exception:
        downloaded_file = wget.download(url, out=gov_file_name)
        file = open(downloaded_file)
    return file

def from_csv_to_json():
    json_res = []
    csv_entry = csv.reader(get_csv(url_gov), delimiter=";")
    count = 0
    for raw in csv_entry:
        if count == 0:
            count=count+1
            continue

        json_res.append(
            json.dumps(
            {
                "Name":raw[3],
                "Id":'',
                "X":re.split(r'[( )]', raw[10])[2],
                "Y":re.split(r'[( )]', raw[10])[1],
                "Type":raw[11],
                "Descript":'',
                "Rating":'',
                "Time":''
            })
        )
    print(json_res)
    return json_res


def db_connect():
    """"
    Функция подключается к базе данных life_game_service_database и возвращает подключение к ней
    """
    try:
        connect = pymysql.connect(host='90.189.132.25',
                                  user='dev_life_user',
                                  password='PINLOX!@#',
                                  db='life_game_service',
                                  cursorclass=pymysql.cursors.DictCursor,
                                  charset='utf8')
        return connect, connect.cursor()
    except:
        print('Fatal error: connect database')
        return -1, -1

def create_table_geo():
    connect, current_connect = db_connect()
    sql = "CREATE TABLE Geo (" \
          "Id int(11) AUTO_INCREMENT, " \
          "Name varchar(256), " \
          "X float(11, 6), " \
          "Y float(11, 6), " \
          "Descript varchar(512), " \
          "Type varchar(64), " \
          "Rating int(11), " \
          "Time int(11) " \
          ") " \
          "ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;"
    print(sql)
    try:
        current_connect.execute(sql)
        connect.commit()
        current_connect.close()
    except:
        print(123)
        return


def add_json_to_sql(json_data):
    connect, current_connect = db_connect()
    if connect == -1:
        return {"Answer": "Warning", "Data": "Ошибка доступа к базе данных, повторить позже"}

    for json_data_single in json_data:
        sql = "INSERT INTO Geo" \
              " VALUES (null, '{}', {}, {}, '{}', '0', 0, 0)".format(
            json.loads(json_data_single)['Name'],
            json.loads(json_data_single)['X'],
            json.loads(json_data_single)['Y'],
            json.loads(json_data_single)['Type']
        )
        print(sql)
        try:
            current_connect.execute(sql)
            connect.commit()
        except:
            print('error: Ошибка запроса к базе данных.')


#create_table_geo()
#get_csv(url_gov)
#add_json_to_sql(from_csv_to_json())