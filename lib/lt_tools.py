'''
提供彩票爬虫相关工具方法及一些彩票共性方法
'''
import random

import requests
from etc import constant
from urllib import parse
from bs4 import BeautifulSoup
import pandas as pd
import ssl
from datetime import datetime

context = ssl.create_default_context()


# 双色球爬虫类
class ssq_tools:

    def __init__(self):
        pass

    # 从福利彩票网站爬取数据
    def get_data_from_flcp(self, dayStart, dayEnd, pageSize, isPrint=False):
        # 构造双色球爬虫网址
        url = parse.urljoin(constant.flcp_base_url, constant.ssq_suffix_url)
        # 构造查询参数
        dict = {
            'name': 'ssq',
            'issueCount': '',
            'issueStart': '',
            'issueEnd': '',
            'dayStart': dayStart,
            'dayEnd': dayEnd,
            'pageNo': '1',
            'pageSize': pageSize,
            'week': '',
            'systemType': 'PC'
        }
        r = requests.get(url, verify=False, params=dict)
        total = r.json()['total']
        now = datetime.now().strftime(constant.specific_format)
        print(f"共爬取 {total} 条数据，当前时间为 {now}")
        results = r.json()['result']
        df = pd.DataFrame(columns=constant.ssq_columns)

        # 将内容以逗号分隔，
        for result in results[-1::-1]:
            seq = ','.join(
                [result['code'], result['date'][0:10], result['blue'], result['red'],
                 result['content'].replace(',', '，'),
                 result['prizegrades'][0]['typemoney']])
            df.loc[len(df.index)] = seq.split(',')

        if isPrint == True:
            df.to_csv('./ssq.csv')

        return df

    # 从kaijiang网站获取历史数据
    def get_data_from_kaijiang(self, startYear=2003, endYear=2012, isPrint=False):

        url = parse.urljoin(constant.kj_base_url, constant.kj_ssq_url)

        df = pd.DataFrame(columns=constant.ssq_columns)
        for year in range(startYear, endYear + 1):
            dict = {
                "startqi": '2003001',
                "endqi": '2013014',
                "year": year,
                "action": 'years'  # years或range
            }

            r = requests.post(url, headers=constant.headers, verify=False, data=dict)

            soup = BeautifulSoup(r.text, 'lxml')

            trs = soup.find_all('tr')
            for tr in trs[-2:1:-1]:
                tr_arr = tr.text.split('\n')
                if ',' in tr_arr[16] or ',' not in tr_arr[17]:
                    i, j = tr_arr[17], tr_arr[18].replace(',', '')
                else:
                    i, j = tr_arr[16], tr_arr[17].replace(',', '')

                seq = ','.join([tr_arr[1], tr_arr[2], tr_arr[11], tr_arr[5], tr_arr[6], tr_arr[7], tr_arr[8], tr_arr[9],
                                tr_arr[10], i, j])

                df.loc[len(df.index)] = seq.split(',')

        return df


# 彩票共性方法
class lt_tools:

    def __init__(self):
        self.r = random.Random()

    # 生成从start到end的length个可重复或不可重复的数，返回长度为n的数组
    def create_randoms_num(self, start, end, length, canRepeat=False):
        thisSeq = []
        while (len(thisSeq) < length):
            nowRedDigit = self.r.randint(start, end)
            if canRepeat:
                thisSeq.append(nowRedDigit)
            elif nowRedDigit not in thisSeq:
                thisSeq.append(nowRedDigit)

        thisSeq.sort()
        return thisSeq

    # 从df中找到与seq有n个数相同的序列，其中df第一列为期数issue，剩下的为二维数
    # 返回期数
    def get_similar_seq(self, df, seq, n=1):
        series = df.pop('issue')  # 删除第一列并返回
        df = df.apply(pd.to_numeric)  # 将剩余df构造为数字类型
        result = series[df.isin(seq).sum(axis=1) == n]
        return result
