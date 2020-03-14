"""
Yash Bardapurkar
1001731650
CSE-6331-004
"""

import pyodbc

server = 'tcp:1650-cse-6331.database.windows.net,1433'
database = '1650-cse-6331'
username = 'ybardapurkar@1650-cse-6331'
password = 'Abcd123456'
driver= '{ODBC Driver 17 for SQL Server}'
try:
	connect = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

except Exception as e:
	print(e)
	connect = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)