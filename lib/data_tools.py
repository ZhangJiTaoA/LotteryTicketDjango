'''
彩票数据相关操作
'''
from lib.sql_tools import connect_mysql
import pandas as pd
from etc import constant
class SSQ_data:
    def __init__(self):
        self.mysql = connect_mysql()

    def get_dataframe(self):
        return pd.read_sql_table(constant.ssq_db_name,con=self.mysql.create_engine())















