import ibm_db

connection = ibm_db.connect('DATABASE=BLUDB;'
	'HOSTNAME=dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net;'
	'PORT=50000;'
	'PROTOCOL=TCPIP;'
	'UID=lts93449;'
	'PWD=50w65gdgxmvpm+f2;', '', '')
