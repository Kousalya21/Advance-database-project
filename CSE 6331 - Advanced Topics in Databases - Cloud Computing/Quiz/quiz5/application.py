from flask import Flask, render_template, request, url_for
from awsdb import conn
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from collections import Counter
import datetime

application = Flask(__name__)

deets = ["Yash Bardapurkar", "1001731650"]
options = { 0: 'CabinNum', 1: 'Fname', 2: 'Lname', 
3: 'Age', 4: 'Height', 5: 'Education', 6: 'wealth',
7: 'Survived', 8: 'Lat', 9: 'Long', 10: 'Fare'}

@application.route('/', methods=["GET"])
def hello_world():
	image = url_for('static', filename='twitter.png')
	return render_template('index.html', image=image, deets=deets)


@application.route('/prob5', methods=["POST"])
def prob5():

	start_time_1 = datetime.datetime.now().timestamp()

	clusterno = 4
	
	cur = conn.cursor()
	sql = "SELECT age, height from minnow where age != '' and height != '';"
	cur.execute(sql)

	npArray = np.array(cur.fetchall())

	k_means = KMeans(n_clusters=clusterno)
	k_means.fit(npArray)

	arr_centroids = k_means.cluster_centers_
	arr_labels = k_means.labels_

	count = Counter(arr_labels)
	number = list(count.items())

	centers1 = []
	centroids = arr_centroids.tolist()
	for i in range(clusterno):
		centers1.append([arr_centroids[i][0], arr_centroids[i][1], number[i][1]])

	total_time_1 = datetime.datetime.now().timestamp() - start_time_1

	start_time_2 = datetime.datetime.now().timestamp()

	clusterno = 3

	cur = conn.cursor()
	sql = "SELECT CabinNum, fare from minnow where CabinNum != '' and fare != '';"
	cur.execute(sql)

	npArray = np.array(cur.fetchall())

	k_means = KMeans(n_clusters=clusterno)
	k_means.fit(npArray)

	arr_centroids = k_means.cluster_centers_
	arr_labels = k_means.labels_

	count = Counter(arr_labels)
	number = list(count.items())

	centers2 = []
	centroids = arr_centroids.tolist()
	for i in range(clusterno):
		centers2.append([arr_centroids[i][0], arr_centroids[i][1], number[i][1]])

	total_time_2 = datetime.datetime.now().timestamp() - start_time_2

	return render_template('prob5.html', centroids1=centers1, centroids2=centers2, time1=total_time_1, time2=total_time_2, deets=deets)


@application.route('/prob6', methods=["POST"])
def prob6():
	clusterno = int(request.form['clusterno'])

	column1 = int(request.form['column1'])
	column2 = int(request.form['column2'])

	cur = conn.cursor()
	sql = "SELECT " +  options[column1] + ", " +  options[column2] + " from minnow where " + options[column1] + " != '' and " + options[column2] + " != '';"
	cur.execute(sql)

	npArray = np.array(cur.fetchall())

	if (column1 == 7 or column1 == 1 or column1 == 2) :
		label_encoder = LabelEncoder()
		npArray[:, 0] = label_encoder.fit_transform(npArray[:, 0])
	if (column2 == 7 or column2 == 2 or column2 == 2) :
		label_encoder = LabelEncoder()
		npArray[:, 1] = label_encoder.fit_transform(npArray[:, 1])

	k_means = KMeans(n_clusters=clusterno)
	k_means.fit(npArray)

	arr_centroids = k_means.cluster_centers_
	arr_labels = k_means.labels_

	count = Counter(arr_labels)
	number = list(count.items())

	centers = []
	centroids = arr_centroids.tolist()
	for i in range(clusterno):
		centers.append([arr_centroids[i][0], arr_centroids[i][1], number[i][1]])


	return render_template('prob6.html', col1=options[column1], col2=options[column2], centroids=centers, deets=deets)


@application.route('/prob7', methods=["POST"])
def prob7():
	clusterno = int(request.form['clusterno'])

	column1 = int(request.form['column1'])
	column2 = int(request.form['column2'])

	cur = conn.cursor()
	sql = "SELECT " +  options[column1] + ", " +  options[column2] + " from minnow where " + options[column1] + " != '' and " + options[column2] + " != '';"
	cur.execute(sql)

	npArray = np.array(cur.fetchall())

	if (column1 == 7 or column1 == 1 or column1 == 2) :
		label_encoder = LabelEncoder()
		npArray[:, 0] = label_encoder.fit_transform(npArray[:, 0])
	if (column2 == 7 or column2 == 2 or column2 == 2) :
		label_encoder = LabelEncoder()
		npArray[:, 1] = label_encoder.fit_transform(npArray[:, 1])

	k_means = KMeans(n_clusters=clusterno)
	k_means.fit(npArray)

	arr_centroids = k_means.cluster_centers_
	arr_labels = k_means.labels_

	count = Counter(arr_labels)
	number = list(count.items())

	centers = []
	centroids = arr_centroids.tolist()
	for i in range(clusterno):
		centers.append([i, arr_centroids[i][0], arr_centroids[i][1], number[i][1]])


	return render_template('prob7.html',column1=column1, column2=column2, clusterno=clusterno, col1=options[column1], col2=options[column2], centroids=centers, deets=deets, person={})

@application.route('/prob7_cluster', methods=["POST"])
def prob7_cluster():
	clusterno = int(request.form['clusterno'])

	column1 = int(request.form['column1'])
	column2 = int(request.form['column2'])

	cur = conn.cursor()
	sql = "SELECT " +  options[column1] + ", " +  options[column2] + " from minnow where " + options[column1] + " != '' and " + options[column2] + " != '';"
	cur.execute(sql)

	npArray = np.array(cur.fetchall())

	if (column1 == 7 or column1 == 1 or column1 == 2) :
		label_encoder = LabelEncoder()
		npArray[:, 0] = label_encoder.fit_transform(npArray[:, 0])
	if (column2 == 7 or column2 == 2 or column2 == 2) :
		label_encoder = LabelEncoder()
		npArray[:, 1] = label_encoder.fit_transform(npArray[:, 1])

	k_means = KMeans(n_clusters=clusterno)
	k_means.fit(npArray)

	arr_centroids = k_means.cluster_centers_
	arr_labels = k_means.labels_

	selected_cluster = int(request.form.get("clusterIndex", -1))
	person = {}
	if selected_cluster > 0:
		index = 0;
		for i in range(len(arr_labels)):
			if arr_labels[i] == selected_cluster:
				index = i
				break
		cur = conn.cursor()
		sql = "SELECT * from minnow where " + options[column1] + " = '" + str(npArray[index][0]) + "' and " + options[column2] + " = '" + str(npArray[index][1]) + "';"
		cur.execute(sql)

		person = cur.fetchone()

	count = Counter(arr_labels)
	number = list(count.items())

	centers = []
	centroids = arr_centroids.tolist()
	for i in range(clusterno):
		centers.append([i, arr_centroids[i][0], arr_centroids[i][1], number[i][1]])
	return render_template('prob7.html',column1=column1, column2=column2, clusterno=clusterno, col1=options[column1], col2=options[column2], centroids=centers, deets=deets, person=person, selected_cluster=selected_cluster)

@application.route('/prob8', methods=["POST"])
def prob8():
	clusterno = int(request.form['clusterno'])

	column1 = int(request.form['column1'])
	column2 = int(request.form['column2'])

	cur = conn.cursor()
	sql = "SELECT " +  options[column1] + ", " +  options[column2] + " from minnow where " + options[column1] + " != '' and " + options[column2] + " != '';"
	cur.execute(sql)

	npArray = np.array(cur.fetchall())

	if (column1 == 7 or column1 == 1 or column1 == 2) :
		label_encoder = LabelEncoder()
		npArray[:, 0] = label_encoder.fit_transform(npArray[:, 0])
	if (column2 == 7 or column2 == 2 or column2 == 2) :
		label_encoder = LabelEncoder()
		npArray[:, 1] = label_encoder.fit_transform(npArray[:, 1])

	k_means = KMeans(n_clusters=clusterno)
	k_means.fit(npArray)

	arr_centroids = k_means.cluster_centers_
	arr_labels = k_means.labels_

	count = Counter(arr_labels)
	number = list(count.items())

	centers = []
	centroids = arr_centroids.tolist()
	for i in range(clusterno):
		centers.append([i, arr_centroids[i][0], arr_centroids[i][1], number[i][1]])


	return render_template('prob8.html', col1=options[column1], col2=options[column2], centroids=centers, deets=deets)


@application.route('/cluster', methods=["POST"])
def stringvalue():
	clusterno = int(request.form['clusterno'])

	column1 = int(request.form['column1'])
	column2 = int(request.form['column2'])

	cur = conn.cursor()
	sql = "SELECT " +  options[column1] + ", " +  options[column2] + " from titanic2 where " + options[column1] + " != '' and " + options[column2] + " != '';"
	cur.execute(sql)

	npArray = np.array(cur.fetchall())

	if (column1 == 9 or column1 == 3 or column1 == 14) :
		label_encoder = LabelEncoder()
		npArray[:, 0] = label_encoder.fit_transform(npArray[:, 0])
	if (column2 == 9 or column2 == 3 or column2 == 14) :
		label_encoder = LabelEncoder()
		npArray[:, 1] = label_encoder.fit_transform(npArray[:, 1])

	k_means = KMeans(n_clusters=clusterno)
	k_means.fit(npArray)

	arr_centroids = k_means.cluster_centers_
	arr_labels = k_means.labels_

	count = Counter(arr_labels)
	number = list(count.items())

	centers = []
	centroids = arr_centroids.tolist()
	for i in range(clusterno):
		centers.append([arr_centroids[i][0], arr_centroids[i][1], number[i][1]])


	return render_template('cluster.html', points=npArray.tolist(), centroids=centers, deets=deets)


@application.route('/centroid_distance', methods=["POST"])
def centroid_distance():
	clusterno = int(request.form['clusterno'])

	column1 = int(request.form['column1'])
	column2 = int(request.form['column2'])

	cur = conn.cursor()
	sql = "SELECT " +  options[column1] + ", " +  options[column2] + " from titanic2 where " + options[column1] + " != '' and " + options[column2] + " != '';"
	cur.execute(sql)

	npArray = np.array(cur.fetchall())

	if (column1 == 9 or column1 == 3) :
		label_encoder = LabelEncoder()
		npArray[:, 0] = label_encoder.fit_transform(npArray[:, 0])
	if (column2 == 9 or column2 == 3) :
		label_encoder = LabelEncoder()
		npArray[:, 1] = label_encoder.fit_transform(npArray[:, 1])


	k_means = KMeans(n_clusters=clusterno)
	k_means.fit(npArray)

	arr_centroids = k_means.cluster_centers_
	arr_labels = k_means.labels_

	distance_table = []
	for i in range(len(arr_centroids)):
		for j in range(len(arr_centroids)):
			dist = np.linalg.norm(arr_centroids[i] - arr_centroids[j])
			distance_table.append([arr_centroids[i], arr_centroids[j], dist])

	
	return render_template('centroid_distance.html', points=npArray.tolist(), distance_table=distance_table, deets=deets)

@application.route('/inertia', methods=["POST"])
def inertia():
	clusterno = int(request.form['clusterno'])

	column1 = int(request.form['column1'])
	column2 = int(request.form['column2'])

	cur = conn.cursor()
	sql = "SELECT " +  options[column1] + ", " +  options[column2] + " from titanic2 where " + options[column1] + " != '' and " + options[column2] + " != '';"
	cur.execute(sql)

	npArray = np.array(cur.fetchall())

	if (column1 == 9 or column1 == 3) :
		label_encoder = LabelEncoder()
		npArray[:, 0] = label_encoder.fit_transform(npArray[:, 0])
	if (column2 == 9 or column2 == 3) :
		label_encoder = LabelEncoder()
		npArray[:, 1] = label_encoder.fit_transform(npArray[:, 1])


	distortions = []
	for k in range(2, clusterno + 1):
		k_means = KMeans(n_clusters=k)
		k_means.fit(npArray)
		distortions.append([k, k_means.inertia_])

	return render_template('inertia.html', distortions=distortions, deets=deets)

# run the app.
if __name__ == '__main__':
	application.debug = True
	application.run()