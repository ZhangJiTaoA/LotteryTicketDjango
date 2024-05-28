import array
import string

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from lib.sql_tools import connect_mysql
from lib.ssq_tools import SSQ
import json
from datetime import datetime
from etc import constant


def query_latest_info(request):
    sql = connect_mysql()
    cursor = sql.GetCursor()
    sql_seq = "select red1, red2, red3,red4, red5, red6, blue ,time,issue  from SSQ where time = (select max(time) from SSQ)"
    cursor.execute(sql_seq)
    result = cursor.fetchone()
    result = list(result)
    date = datetime.strptime(result[7],constant.date_format)
    result.append(date.weekday())
    result_dict = {"1":result}
    return JsonResponse(result_dict)


def query_random_info(request):
    ssq = SSQ()
    # 默认随机生成五条数据
    result = []
    for i in range(5):
        res = ssq.create_ssq()
        result.append(res)
    result_dict = {'1':result}

    return JsonResponse(result_dict)


def query_similar_info(request):
    arr = request.GET.get('arr')
    arr = arr.split(',')
    int_arr = [int(item) for item in arr]

    ssq = SSQ()
    result, n = ssq.query_similar_ssq(int_arr)

    print(f"历史上最多共有{n}球个相同，共{len(result)}条数据，具体数据为{result}")
    json_result = result.to_dict()
    return JsonResponse(json_result)
