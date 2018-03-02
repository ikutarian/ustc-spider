# coding: utf-8

import requests
from bs4 import BeautifulSoup
import json
import csv


def down_html():
    url = 'http://gradschool.ustc.edu.cn/articles/2015/03/18.htm'
    user_agent = {
    }
    r = requests.get(url, headers = user_agent)
    r.encoding = 'gbk'
    with open('ustc.html', 'w') as f:
        f.write(r.text)
        f.close()


def convert_2_json():
    soup = BeautifulSoup(open('ustc.html'), 'lxml')
    trs = soup.find_all('tr', style = 'height:20.1pt')[1:-1]
    infos = []
    for tr in trs:
        spans = tr.find_all('span')
        info = {
            'num': spans[0].string,
            'id': spans[1].string,
            'name': spans[2].string,
            'dept': spans[3].string,
        }
        infos.append(info)
    with open('ustc.json', 'w') as f:
        f.write(json.dumps(infos, ensure_ascii = False, indent = 1))
        f.close()


def calculate_dept_count():
    data_list = json.load(open('ustc.json'))
    dept_count = {}
    for data in data_list:
        dept = data['dept']
        if dept in dept_count.keys():
            count = dept_count[dept]
            count += 1
            dept_count[dept] = count
        else:
            dept_count[dept] = 1
    print('拟录取总人数：{}'.format(len(data_list)))
    print('-' * 20)
    for item in sorted(dept_count.items(), key = lambda item : item[1], reverse = True):
        print('{} = {}'.format(*item))


def get_id_area():
    rows = csv.reader(open('area.csv', encoding = 'utf-8'))
    id_area = {}
    for row in rows:
        id_top_2, area = row[0][:2], row[1]
        if id_top_2 not in id_area.keys():
            id_area[id_top_2] = area
    return id_area


def calculate_area_count():
    id_area = get_id_area()
    data_list = json.load(open('ustc.json'))
    area_count = {}
    for data in data_list:
        area = id_area[data['id'][:2]]
        if area in area_count.keys():
            count = area_count[area]
            count += 1
            area_count[area] = count
        else:
            area_count[area] = 1
    for item in sorted(area_count.items(), key = lambda item : item[1], reverse = True):
        print('{} {}'.format(*item))


if __name__ == '__main__':
    down_html()
    convert_2_json()
    calculate_dept_count()
    calculate_area_count()
