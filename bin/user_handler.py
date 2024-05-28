from lib.sql_tools import connect_mysql

conn = connect_mysql()
cursor = conn.GetCursor()
cursor.execute()




