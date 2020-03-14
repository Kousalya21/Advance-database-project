import pyodbc

server = 'tcp:1650-cse-6331.database.windows.net,1433'
database = '1650-cse-6331'
username = 'ybardapurkar@1650-cse-6331'
password = 'Abcd123456'
driver= '{ODBC Driver 17 for SQL Server}'
try:
	connect = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
	# cursor = conn.cursor()
	# cursor.execute("SELECT * from quakes")
	# row = cursor.fetchone()
	# while row:
	# 	print (str(row))
	# 	row = cursor.fetchone()
except Exception as e:
	print(e)
	connect = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)