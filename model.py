import sqlite3

def get_nb_system(test) :
	#return the number of sample for a test, query to make !
	# in test.db :
	# select count(*) from system
	#get mocked kid !
	return 2

def get_nb_question(test) :
	#return the number of sample for a test, query to make !
	# in static_db :
	# select nb_question from test where test_id = test
	#get mocked kid !
	return 2

def get_nb_step(test) :
	#return the number of step required on a test
	# in static_db :
	# select nb_step from test where test_id = test
	#get mocked kid !
	return 6

def get_nb_step_user(test,user) :
	#return the number of step required on a test
	# get the number of answer of the user
	# in test.db :
	# select count(*) from answer where user = param(user)
	# then devide it by the number of question of the test
	# get_nb_question(test)
	#get mocked kid !
	return 0

def get_metadata(test) :
	conn = sqlite3.connect('databases/'+test+'.db')
	c = conn.cursor()
	c.execute("select * from test where test_id="+test)
	res = c.fetchall()
	conn.close()
	return res[0]

def get_test_sample(test,user) :
	#load a tuple of sample depending of the user and the number of time processed
	conn = sqlite3.connect('databases/'+test+'.db')
	c = conn.cursor()
	c.execute("select * from sample")
	sampleList = c.fetchall()
	nb = sampleList[0]["time-processed"]
	for sample in sampleList :
		#check if user has not already processed this sample
		c.execute("select count(*) from answer where user=\""+user+"\" and system_index="+sample[""]+"")
		#if it is the case then go to the next sample
		#then take the sample which has been processed the fewest time
		if sample["time-processed"] < nb :
			nb = sample["time-processed"]
			#keep the sample
			s1 = "/test_sound/"+test+"/"+sample["path"]
			s2 = "/test_sound/"+test+"/dolphin.wav"
			samples = [{"id" : 1, "path" : s1},{"id" : 2, "path" : s2}]
	s1 = "/test_sound/"+test+"/bird.wav"
	s2 = "/test_sound/"+test+"/dolphin.wav"
	samples = [{"id" : 1, "path" : s1},{"id" : 2, "path" : s2}]
	conn.close()
	return samples

def insert_data(test,data) :
	i=0