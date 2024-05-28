import pymysql
from etc import constant
from sqlalchemy import create_engine


class connect_mysql:

    def __init__(self):
        # 连接到MySQL数据库
        self._conn = pymysql.connect(
            host=constant.host,
            user=constant.username,
            password=constant.password,
            database=constant.database,
            port=constant.port,
            charset=constant.charset
        )
        self._cursor = self._conn.cursor()

    # 返回一个数据库连接
    def GetConnect(self):

        return self._conn

    # 创建游标并返回
    def GetCursor(self):
        return self._cursor

    def create_engine(self):
        return create_engine(constant.engine)

    # 当对象被销毁时关闭游标和连接
    def __del__(self):
        self._cursor.close()
        self._conn.close()


# if __name__ == '__main__':
#     mysql = connect_mysql()
#     mysql.GetConnect()
