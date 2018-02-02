import json

__author__ = 'ar.chusovitin'


def converter(js):
    """
    ����� ��������������� ������������ json � Dict � ��������
    :param js: str ��� json
    :return: str ��� dict ��������������� �������
    """
    return json.dumps(js) if isinstance(js, dict) else json.loads(js)
