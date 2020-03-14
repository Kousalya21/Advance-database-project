import pymysql

host="db-1650-cse-6331.cqbvltbmoqix.us-east-2.rds.amazonaws.com"
port=3306
dbname="db_1650_cse_6331"
user="ybardapurkar"
password="Abcd123456"

connect = pymysql.connect(host, user, password, dbname)