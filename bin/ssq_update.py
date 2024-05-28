# coding=utf-8
'''
更新数据库中ssq数据
'''
import time
from datetime import date, datetime, timedelta
from lib.lt_tools import ssq_tools
from etc import constant
from lib.sql_tools import connect_mysql


def refresh_ssq():
    # 查询数据库中最大的日期为flag_time
    mysql = connect_mysql()
    cursor = mysql.GetCursor()
    sql_seq = "select max(time) from SSQ"
    result = cursor.execute(sql_seq)
    flag_time = cursor.fetchone()[0]

    # 构造时间，并从最大日期的下一天到今天开始爬虫
    flag_time = datetime.strptime(flag_time, constant.date_format).date() + timedelta(days=1)
    result = ssq_tools().get_data_from_flcp(flag_time, date.today(), 2 ** 31 - 1)
    if (result.empty != True):
        result.to_sql(name=constant.ssq_db_name, con=mysql.create_engine(), index=False, if_exists="append")


if __name__ == '__main__':
    refresh_ssq()
    while True:
        now_hour = datetime.now().hour
        now_minute = datetime.now().minute
        now_seconds = datetime.now().second
        # 今天已经过去多少秒
        all_seconds = now_hour * 60 * 60 + now_minute * 60 + now_seconds

        time.sleep(constant.seconds_in_day - all_seconds - 2 * 60 * 60)  # 每天22点
        refresh_ssq()
        time.sleep(30 * 60)  # 每天22：30
        refresh_ssq()
        time.sleep(60 * 60)  # 每天23：30
        refresh_ssq()
        time.sleep(60 * 60)  # 跨越到第二天0：30
