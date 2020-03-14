# import pyodbc

# server = 'db-1650-cse-6331-ms.cqbvltbmoqix.us-east-2.rds.amazonaws.com'
# database = '1650-cse-6331'
# username = 'ybardapurkar@db-1650-cse-6331-ms'
# password = 'Abcd123456'
# driver= '{ODBC Driver 17 for SQL Server}'
# try:
# 	connect = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
# 	# cursor = conn.cursor()
# 	# cursor.execute("SELECT * from quakes")
# 	# row = cursor.fetchone()
# 	# while row:
# 	# 	print (str(row))
# 	# 	row = cursor.fetchone()
# except Exception as e:
# 	print(e)
# 	connect = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
import pymysql

host="db-1650-cse-6331.cqbvltbmoqix.us-east-2.rds.amazonaws.com"
port=3306
dbname="db_1650_cse_6331"
user="ybardapurkar"
password="Abcd123456"

conn = pymysql.connect(host, user, password, dbname)
# conn = pymysql.connect(host, user, password, dbname)

# def connectDB():
#     global con
#     # con = pymysql.connect(host='adb05.ck8bl9unat0f.us-east-2.rds.amazonaws.com', user='admin', password='test1234', db='adb05')
#     con = pymssql.connect('adb05.ck8bl9unat0f.us-east-2.rds.amazonaws.com', 'admin', 'test1234', 'adb05')

# application.add_url_rule('/', 'index', main)