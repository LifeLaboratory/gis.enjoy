# coding=utf-8
def get_from_txt(namefile):
    f = open(namefile)
    text = f.read()
    result = text.split('\n')
    list_js = []
    js = {}
    for i in range(len(result)):
        line = result[i].split(';')
        js["Name"] = line[0]
        js["X"] = line[1]
        js["Y"] = line[2]
        js["Type"] = line[3]
        js["Description"] = line[4]
        js["Rating"] = line[5]
        js["Time"] = line[6]
        js["Max_time"] = line[7]
        list_js.append(js)
        js = {}
    return list_js
