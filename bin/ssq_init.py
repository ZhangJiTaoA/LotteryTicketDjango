'''
ssq数据库初始化
'''
import pandas as pd
from lib.lt_tools import ssq_tools
from datetime import date
from lib.sql_tools import connect_mysql
from etc import constant

if __name__ == '__main__':
    SSQ = ssq_tools()
    df1 = SSQ.get_data_from_flcp(dayStart=date(2013, 1, 1), dayEnd=date.today(), pageSize=2 ** 31 - 1)
    df2 = SSQ.get_data_from_kaijiang(2003, 2012)
    result = pd.concat([df2, df1])
    connect = connect_mysql().create_engine()
    result.to_sql(name=constant.ssq_db_name, con=connect, index=False, if_exists='replace')
