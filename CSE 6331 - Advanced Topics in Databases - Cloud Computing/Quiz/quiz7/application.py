from flask import Flask, render_template, request, url_for
import json, datetime, random
from awsdb import connect
from awsredis import r

application = Flask(__name__)

deets=["Yash Bardapurkar", "1001731650"]

# default
@application.route('/', methods=["GET"])
def hello_world():
	# return render_template('index.html', result=obj)
	return render_template('index.html', deets=deets)


@application.route('/student', methods=["GET"])
def student_view():
	# return render_template('index.html', result=obj)
	return render_template('student.html', deets=deets)

# num = 0

@application.route('/student/my_courses', methods=["POST"])
def student_courses():
	student_id = int(request.form["student_id"])
	# num = num + 1

	sql = "SELECT * from Fall2019 inner join Enrollments on Enrollments.CourseID = Fall2019.Course and Enrollments.Section = Fall2019.Section where Enrollments.StudentID = '" + str(student_id) + "';"
	cursor = connect.cursor()
	cursor.execute(sql)
	output = cursor.fetchall()
	print(output)
	num = 0

	return render_template('student_courses.html', student_id=student_id, courses=output, num=num, deets=deets)


@application.route('/student/enroll', methods=["POST"])
def student_enroll():
	student_id = int(request.form["student_id"])
	course_id = int(request.form["course_id"])
	section = int(request.form["section"])

	sql = "SELECT count(*) from Enrollments where Enrollments.StudentID = '" + str(student_id) + "';"
	cursor = connect.cursor()
	cursor.execute(sql)
	count = cursor.fetchone()[0]

	if count > 0:
		# already enrolled
		print('enrolled')

	sql = "SELECT Course, Section, Max from Fall2019 where Fall2019.Course = '" + str(course_id) + "' and Fall2019.Section = '" + str(section) + "';"
	cursor = connect.cursor()
	cursor.execute(sql)
	course = cursor.fetchone()

	if len(course) == 0:
		# already enrolled
		print('course not found')
		message = "Course not found"
		return render_template('student_enroll.html', message=message, deets=deets)

	sql = "SELECT count(*) from Enrollments where Enrollments.CourseID = '" + str(course_id) + "' and Enrollments.Section = '" + str(section) + "';"
	cursor = connect.cursor()
	cursor.execute(sql)
	count = cursor.fetchone()[0]

	if count >= course[2]:
		print('capacity')
		message = "Section is full"
		return render_template('student_enroll.html', message=message, deets=deets)


	sql = "INSERT INTO Enrollments (StudentID, CourseID, Section) VALUES (" + str(student_id) + ", " + str(course_id) + ", " + str(section) + ");"
	cursor = connect.cursor()
	cursor.execute(sql)

	message = "Success"
	return render_template('student_enroll.html', message=message, deets=deets)

@application.route('/admin', methods=["GET"])
def admin_view():
	# return render_template('index.html', result=obj)
	return render_template('admin.html', deets=deets)

@application.route('/admin/students', methods=["POST"])
def admin_students():
	# return render_template('index.html', result=obj)
	course_id = int(request.form["course_id"])
	section = int(request.form["section"])

	sql = "SELECT * from students inner join Enrollments on Enrollments.StudentID = students.IdNum where Enrollments.CourseID = '" + str(course_id) + "' and Enrollments.Section = '" + str(section) + "';"
	cursor = connect.cursor()
	cursor.execute(sql)
	output = cursor.fetchall()
	print(output)

	return render_template('admin_students.html', course_id=course_id, section=section, students=output, deets=deets)

'''
@application.route('/prob1', methods=["POST"])
def problem_1():

	query_count = int(request.form["query_count"])
	use_cache = (request.form["use_cache"] == "True")

	total_time = 0

	for i in range(query_count):

		if (use_cache):
			# cache
			if r.exists("all"):
				# start time
				start_time = datetime.datetime.now().timestamp()

				result = json.loads(r.get("all"))

				# end time
				total_time = total_time + (datetime.datetime.now().timestamp() - start_time)
			else:

				# start time
				start_time = datetime.datetime.now().timestamp()

				sql = "SELECT place from quakes"
				cursor = connect.cursor()
				cursor.execute(sql)
				output = cursor.fetchall()

				# end time
				total_time = total_time + (datetime.datetime.now().timestamp() - start_time)

				result = []
				for row in output:
					result.append(row[0])

				r.set("all", json.dumps(result))
			
		else:
			# no cache

			# start time
			start_time = datetime.datetime.now().timestamp()

			cursor = connect.cursor()
			sql = "SELECT place from quakes"
			cursor.execute(sql)
			output = cursor.fetchall()

			# end time
			total_time = total_time + (datetime.datetime.now().timestamp() - start_time)

			result = []
			for row in output:
				result.append(row[0])

	total_time = total_time * 1000
	return render_template('prob2.html', query_count=query_count, use_cache=use_cache, execution_time=total_time, deets=deets)

'''
@application.route('/prob5', methods=["POST"])
def problem_2():
	start_magnitude = int(request.form["start_magnitude"])
	end_magnitude = int(request.form["end_magnitude"])

	query_count = int(request.form["query_count"])
	use_cache = (request.form["use_cache"] == "True")

	total_time = 0

	for i in range(query_count):
		magnitude = round(random.uniform(start_magnitude, end_magnitude), 1)

		if (use_cache):
			# cache
			if r.exists("mag=" + str(magnitude)):
				# start time
				start_time = datetime.datetime.now().timestamp()

				result = json.loads(r.get("mag=" + str(magnitude)))

				# end time
				total_time = total_time + (datetime.datetime.now().timestamp() - start_time)
			else:

				# start time
				start_time = datetime.datetime.now().timestamp()

				sql = "SELECT place from quakes where mag = '" + str(magnitude) + "';"
				cursor = connect.cursor()
				cursor.execute(sql)
				output = cursor.fetchall()

				# end time
				total_time = total_time + (datetime.datetime.now().timestamp() - start_time)

				result = []
				for row in output:
					result.append(row[0])

				r.set("mag=" + str(magnitude), json.dumps(result))
			
		else:
			# no cache

			# start time
			start_time = datetime.datetime.now().timestamp()

			cursor = connect.cursor()
			sql = "SELECT place from quakes where mag = '" + str(magnitude) + "';"
			cursor.execute(sql)
			output = cursor.fetchall()

			# end time
			total_time + (datetime.datetime.now().timestamp() - start_time)

			result = []
			for row in output:
				result.append(row[0])

	total_time = total_time * 1000
	return render_template('prob2.html', query_count=query_count, use_cache=use_cache, execution_time=total_time, deets=deets)


@application.route('/prob6', methods=["GET", "POST"])
def problem_6():
	recd = datetime.datetime.now()
	start = recd.timestamp()

	time = round(int(recd.strftime('%f')) / 1000)
	image = ''
	if time % 10 == 0:
		image = url_for('static', filename='a.jpg')
	else:
		image = url_for('static', filename='b.jpg')

	resp = datetime.datetime.now()
	end = resp.timestamp()

	elapsed = (resp.timestamp() - recd.timestamp())

	return render_template('prob6.html', image=image, start=str(start), end=str(end), elapsed=elapsed, deets=deets)





if __name__ == '__main__':
	application.debug = True
	application.run()