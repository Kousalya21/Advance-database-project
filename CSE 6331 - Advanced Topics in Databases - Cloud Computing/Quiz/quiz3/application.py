"""Cloud Foundry test"""
from flask import Flask, current_app, render_template, request, redirect, url_for
import os, json, datetime, random
from azuredb import connect
from azureredis import r

app = Flask(__name__)

print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))

# default
@app.route('/', methods=["GET"])
def hello_world():
	# return render_template('index.html', result=obj)
	return render_template('index.html')

@app.route('/prob5', methods=["POST"])
def problem5():
	start_latitude = float(request.form["start_latitude"])
	end_latitude = float(request.form["end_latitude"])

	if (start_latitude < end_latitude):
		return "start magnitude must be greater than end magnitude"

	cursor = connect.cursor()
	sql = "SELECT time, place, mag, time from quake3 where latitude between ? and ?"
	cursor.execute(sql, (end_latitude, start_latitude))

	result = []
	for row in cursor.fetchall():
		result.append([row[0], row[1], row[2]])

	return render_template('prob5.html', result=result)


@app.route('/prob6', methods=["POST"])
def problem6():
	query_count = int(request.form["query_count"])

	inp1 = float(request.form["inp1"])
	inp2 = float(request.form["inp2"])

	result = []
	i = 0

	for i in range(query_count):

		latitude1 = round(random.uniform(inp2, inp1), 1)
		latitude2 = round(random.uniform(inp2, inp1), 1)

		if (latitude1 > latitude2):
			start_latitude = latitude1
			end_latitude = latitude2
		else:
			start_latitude = latitude2
			end_latitude = latitude1

		# start
		start_time = datetime.datetime.now().timestamp()

		cursor = connect.cursor()
		sql = "SELECT time, place, mag, time from quake3 where latitude between ? and ?"
		cursor.execute(sql, (end_latitude, start_latitude))

		# end time
		total_time = (datetime.datetime.now().timestamp() - start_time)

		result.append({
			"numbers": str(end_latitude) + " to " + str(start_latitude),
			"count": str(len(cursor.fetchall())),
			"time": str(total_time * 1000)
			})

	return render_template('prob6.html', result=result)


@app.route('/prob7', methods=["POST"])
def problem7():
	query_count = int(request.form["query_count"])

	inp1 = float(request.form["inp1"])
	inp2 = float(request.form["inp2"])

	result = []
	i = 0

	for i in range(query_count):

		latitude1 = round(random.uniform(inp2, inp1), 1)
		latitude2 = round(random.uniform(inp2, inp1), 1)

		if (latitude1 > latitude2):
			start_latitude = latitude1
			end_latitude = latitude2
		else:
			start_latitude = latitude2
			end_latitude = latitude1

		# start
		start_time = datetime.datetime.now().timestamp()

		key = 'q3_mag_' + str(end_latitude) + '_' + str(start_latitude)

		output = []
		if r.exists(key):
			output = json.loads(r.get(key))
		else:
			cursor = connect.cursor()
			sql = "SELECT time, place, mag, time from quake3 where latitude between ? and ?"
			cursor.execute(sql, (end_latitude, start_latitude))

			output = []
			for row in cursor.fetchall():
				output.append([row[0], row[1], row[2]])

			r.set(key, json.dumps(output))

		# end time
		total_time = (datetime.datetime.now().timestamp() - start_time)

		result.append({
			"numbers": str(end_latitude) + " to " + str(start_latitude),
			"count": str(len(output)),
			"time": str(total_time * 1000)
			})

	return render_template('prob7.html', result=result)


@app.route('/prob8', methods=["POST"])
def problem8():
	query_count = int(request.form["query_count"])

	inp1 = float(request.form["inp1"])
	inp2 = float(request.form["inp2"])

	use_cache = (request.form["use_cache"] == "True")

	result = []
	i = 0

	for i in range(query_count):

		latitude1 = round(random.uniform(inp2, inp1), 1)
		latitude2 = round(random.uniform(inp2, inp1), 1)

		if (latitude1 > latitude2):
			start_latitude = latitude1
			end_latitude = latitude2
		else:
			start_latitude = latitude2
			end_latitude = latitude1

		# start
		start_time = datetime.datetime.now().timestamp()

		key = 'q3_mag_' + str(end_latitude) + '_' + str(start_latitude)

		output = []
		if (use_cache and r.exists(key)):
			output = json.loads(r.get(key))
		else:
			cursor = connect.cursor()
			sql = "SELECT time, place, mag, time from quake3 where latitude between ? and ?"
			cursor.execute(sql, (end_latitude, start_latitude))

			output = []
			for row in cursor.fetchall():
				output.append([row[0], row[1], row[2]])

			r.set(key, json.dumps(output))

		# end time
		total_time = (datetime.datetime.now().timestamp() - start_time)

		result.append({
			"numbers": str(end_latitude) + " to " + str(start_latitude),
			"count": str(len(output)),
			"time": str(total_time * 1000)
			})

	return render_template('prob8.html', result=result)



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)



