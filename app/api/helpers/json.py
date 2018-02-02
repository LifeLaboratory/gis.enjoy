import json

__author__ = 'ar.chusovitin'


def converter(js):
    """
    Метод преобразовывает передаваемый json в Dict и наоборот
    :param js: str или json
    :return: str или dict преобразованный элемент
    """
    return json.dumps(js) if isinstance(js, dict) else json.loads(js)
