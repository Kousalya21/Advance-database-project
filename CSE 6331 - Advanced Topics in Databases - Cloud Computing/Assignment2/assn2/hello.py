"""Cloud Foundry test"""
from flask import Flask, current_app, render_template, request, redirect, url_for
import os, json, datetime
import ibm_db

import connect

app = Flask(__name__)

print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))

# default
@app.route('/', methods=["GET"])
def hello_world():
	obj = {}

	# for prob 2
	date_range = connect.get_day_range()
	obj["startdate"] = db_to_datetime(date_range["STARTDATE"]).replace(hour=0, minute=0, second=0, microsecond=0)
	obj["enddate"] = db_to_datetime(date_range["ENDDATE"]).replace(hour=23, minute=59, second=59, microsecond=999999)

	return render_template('index.html', result=obj)


# Search for and count all earthquakes that occurred 
# with a magnitude greater than 5.0
@app.route('/prob1', methods=["POST"])
def problem_1():
	magnitude = request.form["magnitude"]
	ret = connect.mag_greater_than(magnitude)
	return render_template('prob1.html', result=ret)


# Search for 2.0 to 2.5, 2.5 to 3.0, etc magnitude quakes 
# for a one week, a range of days or the whole 30 days.
@app.route('/prob2', methods=["POST"])
def problem_2():
	start_magnitude = request.form["start_magnitude"]
	end_magnitude = request.form["end_magnitude"]

	if (start_magnitude > end_magnitude):
		return "start magnitude greater than end magnitude"

	if (request.form["dates"] == "all"):
		ret = connect.mag_in_ranges(start_magnitude, end_magnitude)
	elif (request.form["dates"] == "date"):
		start_range = datetime.datetime.strptime(request.form["start_range"], "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
		end_range = datetime.datetime.strptime(request.form["end_range"], "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=999999).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

		if (start_range is None):
			return "start date required"
		if (end_range is None):
			return "end date required"
		if (start_range > end_range):
			return "start date greater than end date"

		ret = connect.mag_in_ranges_and_dates(start_magnitude, end_magnitude, start_range, end_range)
	else:
		ret = []

	return render_template('prob2.html', result=ret)


def db_to_datetime(datetime_str):
	return datetime.datetime.strptime(datetime_str.strip().replace('T', ' ').replace('Z', ' ') + "000", '%Y-%m-%d %H:%M:%S.%f')


@app.route('/prob3', methods=["POST"])
def problem_3():
	latitude = request.form["latitude"]
	longitude = request.form["longitude"]
	distance = request.form["distance"]

	ret = connect.distance_from_coordinates(latitude, longitude, distance)
	return render_template('prob3.html', result=ret)


@app.route('/prob4', methods=["POST"])
def problem_4():
	start_latitude = float(request.form["start_latitude"])
	start_longitude = float(request.form["start_longitude"])

	end_latitude = float(request.form["end_latitude"])
	end_longitude = float(request.form["end_longitude"])

	step = float(request.form["step"])

	if (start_latitude > 90 or start_latitude < -90):
		return "start latitude out of bounds"
	if (end_latitude > 90 or end_latitude < -90):
		return "end latitude out of bounds"
	if (start_longitude > 180 or start_longitude < -180):
		return "start latitude out of bounds"
	if (end_longitude > 180 or end_longitude < -180):
		return "start latitude out of bounds"

	if (start_latitude < end_latitude):
		return "start latitude should be higher than end latitude"
	if (start_longitude > end_longitude):
		return "start longitude should be lower than end longitude"

	res = []
	max_quakes = 0
	max_latitude = 0
	max_longitude = 0

	latitude = start_latitude
	lats = []
	while latitude > end_latitude:
		longitude = start_longitude
		longs = []
		while longitude < end_longitude:
			cnt = int(connect.cluster_count(latitude, longitude, step)["1"])
			st = ''
			st = st + str(latitude) + 'N ' + str(longitude) + 'W: '
			st = st + str(cnt)
			# longs.append(st)
			longs.append(cnt)
			longitude = longitude + step

			if (cnt > max_quakes):
				max_quakes = cnt
				max_latitude = latitude
				max_longitude = longitude
			
		lats.append(longs)
		latitude = latitude - step
	res.append(lats)

	ret = {}
	ret["latitude"] = start_latitude
	ret["longitude"] = start_longitude
	ret["data"] = res[0]
	ret["max_quakes"] = max_quakes
	ret["max_latitude"] = max_latitude
	ret["max_longitude"] = max_longitude
	ret["step"] = step
	return render_template('prob4.html', result=ret)


@app.route('/prob5', methods=["POST"])
def problem_5():
	ret = connect.mag_greater_than(4)
	total = 0
	day = 0
	night = 0
	for item in ret:
		date = db_to_datetime(item["TIME"])
		longitude = item["LONGITUDE"]
		# print("before " + str(date))
		# print("long = " + str(longitude))
		# print("delta = " + str(int(float(item["LONGITUDE"]) * 4)) + " minutes")
		date = date + datetime.timedelta(minutes=int(float(item["LONGITUDE"]) * 4))
		# print("after " + str(date))
		# print("")
		if (date.hour > 6 and date.hour <= 18):
			day = day + 1
		else:
			night = night + 1
		total = total + 1
	obj = []
	obj.append("day = " + str(day))
	obj.append("night = " + str(night))
	obj.append("total = " + str(total))
	obj.append("day% = " + str(day*1.0/total))
	obj.append("night% = " + str(night*1.0/total))
	# obj.append(datetime.datetime.now())
	# obj.append(datetime.datetime.now() + datetime.timedelta(minutes=70))
	return render_template('prob5.html', result=obj)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)

