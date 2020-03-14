"""Cloud Foundry test"""
from flask import Flask, current_app, render_template, request
import os, json
import ibm_db

import connect

app = Flask(__name__)

print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))

# default
@app.route('/', methods=["GET"])
def hello_world():
	return render_template('index.html')

# open search page
@app.route('/search', methods=["GET"])
def search():
	return render_template('room_search.html')

# search 
@app.route('/room_search', methods=["POST"])
def room_search():
	room = request.form["room"]

	sql = "SELECT * FROM quiz_0_people WHERE 'room' = ?"
	stmt = ibm_db.prepare(connect.connection, sql)

	ibm_db.bind_param(stmt, 1, room)
	result = ibm_db.execute(stmt)

	ret = [];
	result_dict = ibm_db.fetch_assoc(stmt)
	print(json.dumps(result_dict))	
	return render_template('search.html', result=result_dict[picture])

@app.route('/points_search', methods=["POST"])
def points_search():
	start = request.form["start_points"]
	end = request.form["end_points"]

	sql = "SELECT * FROM quiz_0_people WHERE 'points' > ? and points < ?"
	stmt = ibm_db.prepare(connect.connection, sql)

	ibm_db.bind_param(stmt, 1, start)
	ibm_db.bind_param(stmt, 2, end)
	result = ibm_db.execute(stmt)

	ret = [];
	result_dict = ibm_db.fetch_assoc(stmt)

	while result_dict is not False:
		print(json.dumps(result_dict))
		ret.append(result_dict)
		result_dict = ibm_db.fetch_assoc(stmt)
	return render_template('search.html', result=ret)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)

