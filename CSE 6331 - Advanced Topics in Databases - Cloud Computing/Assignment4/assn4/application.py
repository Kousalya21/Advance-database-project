"""
Yash Bardapurkar
1001731650
CSE-6331-004
"""

from flask import Flask, current_app, render_template, request, redirect, url_for
import os, json, datetime, random
from azuredb import connect
from azureredis import r

app = Flask(__name__)

print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))

def mag_range_count(magnitude):
	sql = "SELECT count(*) from quakes where mag >= ? and mag < ?"
	cursor = connect.cursor()
	cursor.execute(sql, (magnitude, magnitude + 1))

	columns = [column[0] for column in cursor.description]
	result = []
	return cursor.fetchone()[0]

# default
@app.route('/', methods=["GET"])
def hello_world():
	# return render_template('index.html', result=obj)
	return render_template('index.html')


def get_magnitude_data():
	sql = """
	select t.range as magnitudes, count(*) as occurences from (
		select case  
			when mag >= 0 and mag < 1 then 0
			when mag >= 1 and mag < 2 then 1
			when mag >= 2 and mag < 3 then 2
			when mag >= 3 and mag < 4 then 3
			when mag >= 4 and mag < 5 then 4
			when mag >= 5 and mag < 6 then 5
			when mag >= 6 and mag < 7 then 6
			when mag >= 7 and mag < 8 then 7
			when mag >= 8 and mag < 9 then 8
			when mag >= 9 and mag < 10 then 9
			else -1 end as range
		from quakes) t
	group by t.range order by magnitudes;
	"""
	cursor = connect.cursor()
	cursor.execute(sql)
	cursor.fetchone()
	return cursor.fetchall()

@app.route('/pie_chart', methods=["POST"])
def pie_chart():
	result = get_magnitude_data()
	return render_template('pie_chart.html', result=result)


@app.route('/bar_chart', methods=["POST"])
def bar_chart():
	result = get_magnitude_data()
	return render_template('bar_chart.html', result=result)


@app.route('/scatter_plot', methods=["POST"])
def scatter_plot():
	# latitude = float(request.form["latitude"])
	# longitude = float(request.form["longitude"])

	# if (latitude > 90 or latitude < -90):
	# 	return "latitude out of bounds"

	# if (longitude > 180 or longitude < -180):
	# 	return "longitude out of bounds"

	# step = 5

	sql = "select latitude, longitude, mag from quakes"# where latitude between ? and ? and longitude between ? and ?;"
	cursor = connect.cursor()
	cursor.execute(sql)#, (latitude - step, latitude + step, longitude - step, longitude + step))

	result = cursor.fetchall();
	# max_latitude = -90
	# max_longitude = -180
	# min_latitude = 90
	# min_longitude = 180

	# result = cursor.fetchall()
	# for item in result:
	# 	if item[0] > max_latitude:
	# 		max_latitude = item[0]
	# 	if item[1] > max_longitude:
	# 		max_longitude = item[1]
	# 	if item[0] < min_latitude:
	# 		min_latitude = item[0]
	# 	if item[1] < min_longitude:
	# 		min_longitude = item[1]

	# margin = 5
	# latitude_range = [int(min_latitude) - margin, int(max_latitude) + margin] if (max_latitude > min_latitude) else [-margin, margin]
	# longitude_range = [int(min_longitude) - margin, int(max_longitude) + margin] if (max_longitude > min_longitude) else [-margin, margin]
	# return render_template('prob3.html', result=result, size=len(result), latitude_range=latitude_range, longitude_range =longitude_range)
	return render_template('scatter_plot.html', result=result, size=len(result))#, latitude_range=latitude_range, longitude_range =longitude_range)


@app.route('/line_chart', methods=["POST"])
def line_chart():
	sql = 'SELECT substring(time, 1, 10) as date, count(*) as occurences from quakes group by substring(time, 1, 10) order by date'
	cursor = connect.cursor()
	cursor.execute(sql)

	return render_template('line_chart.html', result=cursor.fetchall())


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)



