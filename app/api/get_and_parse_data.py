# encoding: utf-8
import csv
import json
import pymysql
import wget
import re
from pprint import pprint
from app.api.get_google_dist import get_google
from api.helpers.service import Gis as gs
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

def add_new_point(new_point):
    sql = " INSERT INTO Geo (Name, X, Y, Type, Descript, Rating, Time) VALUES (\'{}\', {}, {}, \'{}\', \'{}\', {}, {})".format(
        new_point["Name"], float(new_point["X"]), float(new_point["Y"]), new_point["Type"], new_point["Description"], int(new_point["Rating"]), int(new_point["Time"]))
    print(sql)
    gs.SqlQuery(sql)

    sql = "SELECT id FROM Geo WHERE X={} AND Y={}".format(new_point["X"], new_point["Y"])
    new_point["id"] = gs.SqlQuery(sql)
    new_point["id"] = int(new_point["id"][0]['id'])
    #print(new_point["id"][0]['id'])
    points = gs.SqlQuery("SELECT id, x, y FROM Geo WHERE id <> (SELECT last_value from geo_id_seq)")
    for i in range(len(points)):
        data = []
        disti = ""
        distj = ""
        disti = str(points[i]['x']) + "," + str(points[i]['y'])
        distj = str(new_point['X']) + "," + str(new_point['Y'])
        data.append(disti)
        data.append(distj)
        #print(data)
        answer = get_google(data)
        print(points[i]['id'], new_point['id'], answer)
        sql = "INSERT INTO geo_distance (point_1, point_2, distance)" \
                  " VALUES ({}, {}, {})".format(
                points[i]['id'],
                new_point['id'],
                answer)
        #print(sql)
        gs.SqlQuery(sql)

        gs.SqlQuery("INSERT INTO geo_distance (point_1, point_2, distance)" \
                 " VALUES ({}, {}, {})".format(
            new_point['id'],
            points[i]['id'],
            answer))



def get_from_txt():
    f = open('/home/raldenprog/gis.enjoy/app/api/Spb.txt')
    text = f.read()
    #text = text.split("\n")
    result = text.split('\n')
    #pprint(result)
    list_js = []
    js = {}
    for i in range(len(result)):
        line = result[i].split(';')
        #print(line)
        js["Name"] = line[0]
        js["X"] = line[1]
        js["Y"] = line[2]
        js["Type"] = line[3]
        js["Description"] = line[4]
        js["Rating"] = line[5]
        js["Time"] = line[6]
        #print(js)
        #print(len(line))
        js["Max_time"] = line[7]
        #pprint(js)
        list_js.append(js)
        js = {}
        #pprint(list_js)
    return list_js
result = get_from_txt()
#pprint(result)
for i in result:
    print(add_new_point(i))