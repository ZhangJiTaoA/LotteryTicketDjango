from django.shortcuts import render
from django.http import JsonResponse
from etc import constant
from lib.sql_tools import connect_mysql
import requests
from datetime import datetime


# Create your views here.

# 用户登录——通过自己服务器
# def login(request):
#     print(datetime.now().strftime(constant.specific_format))
#     code = request.GET.get("code")
#     print(code)
#     result_json = getOpenid(code)
#     user_info = queryUserByOpenid(result_json)
#     flag = None
#     if ("logintime" in user_info.keys()):  # 如果查询到用户信息则返回以下内容
#         print(user_info)
#     else:  # 没有用户信息则插入用户信息。
#         flag = insertUser(user_info['openid'], user_info['session_key'], constant.init_score, logintime=datetime.now().strftime(constant.specific_format))
#     user_info["insert"] = flag
#     return JsonResponse(user_info)

def login(request):
    print(datetime.now().strftime(constant.specific_format))
    print(request.headers)
    openid = request.headers.get("X-WX-OPENID")

    result_json = {
        'openid': request.headers.get("X-WX-OPENID"),
        'session_key': ''
    }
    user_info = queryUserByOpenid(result_json)
    flag = None
    if ("logintime" in user_info.keys()):  # 如果查询到用户信息则返回以下内容
        print(user_info)
    else:  # 没有用户信息则插入用户信息。
        flag = insertUser(user_info['openid'], user_info['session_key'], constant.init_score, logintime=datetime.now().strftime(constant.specific_format))
    user_info["insert"] = flag
    return JsonResponse(user_info)





def getOpenid(code):
    query_dict = {
        "appid": constant.appid,
        "secret": constant.appsecret,
        "js_code": code,
        "grant_type": "authorization_code"
    }
    r = requests.get(constant.code2Session_url, params=query_dict)
    print(r.json())
    return r.json()


# 参数r为请求微信服务器获取到的json格式数据，包括session_key,openid,也许还有unionid
def queryUserByOpenid(r):
    query_seq = f"select * from User where openid=%s"
    print(query_seq)
    sql = connect_mysql()
    cursor = sql.GetCursor()
    try:
        cursor.execute(query_seq, r['openid'])
        result = dict(zip(constant.user, cursor.fetchone()))
    except:
        return r
    return result


def insertUser(openid, session_key, score, logintime, unionid="", gender=-1, age=-1, ):
    insert_seq = "insert into User(openid, session_key,score,logintime,unionid,gender,age) values(%s,%s,%s,%s ,%s,%s,%s)"
    param = (openid, session_key, score, logintime, unionid, gender, age)
    sql = connect_mysql()
    connect = sql.GetConnect()
    cursor = sql.GetCursor()
    try:
        cursor.execute(insert_seq, param)
        connect.commit()
    except:
        return False

    return True
