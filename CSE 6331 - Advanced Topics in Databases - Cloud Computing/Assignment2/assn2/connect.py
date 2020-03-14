import ibm_db, os, json

# if 'VCAP_SERVICES' in os.environ:
# 	db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB'][0]
# 	db2cred = db2info["credentials"]
# 	appenv = json.loads(os.environ['VCAP_APPLICATION'])
# else:
# 	raise ValueError('Expected cloud environment')

# connection = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")

connection = ibm_db.connect('DATABASE=BLUDB;'
	'HOSTNAME=dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net;'
	'PORT=50000;'
	'PROTOCOL=TCPIP;'
	'UID=lts93449;'
	'PWD=50w65gdgxmvpm+f2;', '', '')


# Search for and count all earthquakes that occurred 
# with a magnitude greater than 5.0
def mag_greater_than(magnitude):
	sql = "SELECT id,place,mag,time,latitude,longitude,depth from ( select mag, REPLACE(REPLACE(TIME, 'Z', ' '), 'T', ' ') as time,id,latitude,longitude,depth,place from earthquakes ) where mag >= ?;"
	stmt = ibm_db.prepare(connection, sql)
	ibm_db.bind_param(stmt, 1, magnitude)
	result = ibm_db.execute(stmt)

	ret = [];
	result_dict = ibm_db.fetch_assoc(stmt)
	while result_dict is not False:
		ret.append(result_dict)
		result_dict = ibm_db.fetch_assoc(stmt)

	return ret


# Search for and count all earthquakes that occurred 
# with a magnitude greater than 5.0
def mag_in_ranges(start_magnitude, end_magnitude):
	sql = "SELECT * from earthquakes where mag between ? and ?;"
	stmt = ibm_db.prepare(connection, sql)
	ibm_db.bind_param(stmt, 1, start_magnitude)
	ibm_db.bind_param(stmt, 2, end_magnitude)
	result = ibm_db.execute(stmt)

	ret = [];
	result_dict = ibm_db.fetch_assoc(stmt)
	while result_dict is not False:
		ret.append(result_dict)
		result_dict = ibm_db.fetch_assoc(stmt)

	return ret


def mag_in_ranges_and_dates(start_magnitude, end_magnitude, start_date, end_date):
	sql = "SELECT * from earthquakes where mag between ? and ? and REPLACE(REPLACE(TIME, 'Z', ' '), 'T', ' ') between ? and ?;"
	stmt = ibm_db.prepare(connection, sql)
	ibm_db.bind_param(stmt, 1, start_magnitude)
	ibm_db.bind_param(stmt, 2, end_magnitude)
	ibm_db.bind_param(stmt, 3, start_date)
	ibm_db.bind_param(stmt, 4, end_date)
	result = ibm_db.execute(stmt)

	ret = [];
	result_dict = ibm_db.fetch_assoc(stmt)
	while result_dict is not False:
		ret.append(result_dict)
		result_dict = ibm_db.fetch_assoc(stmt)

	return ret


def get_day_range():
	sql = """
	SELECT MIN(REPLACE(REPLACE(TIME, 'Z', ' '), 'T', ' ')) as startDate, 
	MAX(REPLACE(REPLACE(TIME, 'Z', ' '), 'T', ' ')) as endDate FROM earthquakes;
	"""
	stmt = ibm_db.prepare(connection, sql)
	result = ibm_db.execute(stmt)
	return ibm_db.fetch_assoc(stmt)

def distance_from_coordinates(latitude, longitude, distance_km):
	# sql = """SELECT (2 * 3961 * asin(sqrt(power((sin(radians((0 - latitude) / 2))), 2) + cos(radians(latitude)) * cos(radians(0)) * power((sin(radians((0 - longitude) / 2))), 2))) as 'dist' from earthquakes where dist <= 20;"""
	sql = "SELECT id,place,mag,time,latitude,longitude,depth,distance from (SELECT id,mag,time,latitude,longitude,depth,place,CAST(SQRT(POW(69.1 * (latitude - ?), 2) +POW(69.1 * (?- longitude) * COS(latitude / 57.3), 2)) AS INT) AS distance  FROM earthquakes) where distance <= ?"
	stmt = ibm_db.prepare(connection, sql)
	ibm_db.bind_param(stmt, 1, latitude)
	ibm_db.bind_param(stmt, 2, longitude)
	ibm_db.bind_param(stmt, 3, distance_km)
	result = ibm_db.execute(stmt)

	ret = [];
	result_dict = ibm_db.fetch_assoc(stmt)
	while result_dict is not False:
		ret.append(result_dict)
		result_dict = ibm_db.fetch_assoc(stmt)

	return ret

def cluster_count(latitude, longitude, step):
	sql = "select count(*) from earthquakes where latitude between ? and ? and longitude between ? and ?"
	stmt = ibm_db.prepare(connection, sql)
	ibm_db.bind_param(stmt, 1, float(latitude) - step)
	ibm_db.bind_param(stmt, 2, float(latitude))
	ibm_db.bind_param(stmt, 3, float(longitude))
	ibm_db.bind_param(stmt, 4, float(longitude) + step)
	result = ibm_db.execute(stmt)

	return ibm_db.fetch_assoc(stmt)

# def list_all():
# 	sql = "SELECT * FROM people;"
# 	stmt = ibm_db.prepare(connection, sql)
# 	result = ibm_db.execute(stmt)

# 	ret = [];
# 	result_dict = ibm_db.fetch_assoc(stmt)
# 	while result_dict is not False:
# 		ret.append(result_dict)
# 		result_dict = ibm_db.fetch_assoc(stmt)

# 	return ret

# def find_by_name(name):
# 	sql = "SELECT * FROM people WHERE name = ?"
# 	stmt = ibm_db.prepare(connection, sql)
# 	ibm_db.bind_param(stmt, 1, name)
# 	result = ibm_db.execute(stmt)

# 	ret = [];
# 	result_dict = ibm_db.fetch_assoc(stmt)
# 	while result_dict is not False:
# 		ret.append(result_dict)
# 		result_dict = ibm_db.fetch_assoc(stmt)

# 	return ret

# def find_by_salary(start, end):
# 	sql = "SELECT * FROM people WHERE salary > ? and salary < ?"
# 	stmt = ibm_db.prepare(connection, sql)
# 	ibm_db.bind_param(stmt, 1, start)
# 	ibm_db.bind_param(stmt, 2, end)
# 	result = ibm_db.execute(stmt)

# 	ret = [];
# 	result_dict = ibm_db.fetch_assoc(stmt)
# 	while result_dict is not False:
# 		ret.append(result_dict)
# 		result_dict = ibm_db.fetch_assoc(stmt)

# 	return ret

# def add_new_people(name, salary, room, keywords, telnum):
# 	sql = "INSERT INTO people(name, salary, room, keywords, telnum) VALUES(?,?,?,?,?)"
# 	stmt = ibm_db.prepare(connect.connection, sql)
# 	ibm_db.bind_param(stmt, 1, name)
# 	ibm_db.bind_param(stmt, 2, salary)
# 	ibm_db.bind_param(stmt, 3, room)
# 	ibm_db.bind_param(stmt, 4, keywords)
# 	ibm_db.bind_param(stmt, 5, telnum)
# 	return ibm_db.execute(stmt)

# def delete_by_name(name):
# 	sql = "DELETE FROM people WHERE name = ?"
# 	stmt = ibm_db.prepare(connection, sql)
# 	ibm_db.bind_param(stmt, 1, name)

# 	return ibm_db.execute(stmt)

# def update_people(old_name, name, salary, room, keywords, telnum):
# 	sql = "UPDATE people SET name = ?, salary = ?, room = ?, keywords = ?, telnum = ? WHERE name = ?"
# 	stmt = ibm_db.prepare(connection, sql)
# 	ibm_db.bind_param(stmt, 1, name)
# 	ibm_db.bind_param(stmt, 2, salary)
# 	ibm_db.bind_param(stmt, 3, room)
# 	ibm_db.bind_param(stmt, 4, keywords)
# 	ibm_db.bind_param(stmt, 5, telnum)
# 	ibm_db.bind_param(stmt, 6, old_name)

# 	return ibm_db.execute(stmt)

# def update_picture(name, picture):
# 	sql = "UPDATE people SET picture = ? WHERE name = ?"
# 	stmt = ibm_db.prepare(connection, sql)
# 	ibm_db.bind_param(stmt, 1, picture)
# 	ibm_db.bind_param(stmt, 2, name)

# 	return ibm_db.execute(stmt)

# 2 * 3961 * asin(sqrt(power((sin(radians((inpLat - latitude) / 2))), 2) + cos(radians(latitude)) * cos(radians(inpLat)) * power((sin(radians((inpLong - longitude) / 2))), 2)))



# SELECT place,mag,time,latitude,longitude,distance from (SELECT mag,time,latitude,longitude,place,CAST(SQRT(POW(69.1 * (latitude - '"+locationLat+"'), 2) +POW(69.1 * ('"+locationLong+"'- longitude) * COS(latitude / 57.3), 2)) AS INT) AS distance  FROM DSQ63569.earthquakes) where distance <= '"+distance+"';