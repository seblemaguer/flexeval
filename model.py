import sqlite3
from datetime import date, datetime

def get_nb_system(test) :
	#return the number of sample for a test, query to make !
	# in test.db :
	# select count(*) from system
	#get mocked kid !
	conn = sqlite3.connect('databases/'+str(test)+'.db')
	c = conn.cursor()
	c.execute("select count(*) from system")
	res = c.fetchall()
	conn.close()
	return res[0][0]

def get_nb_question(test) :
	#return the number of sample for a test, query to make !
	# in static_db :
	# select nb_question from test where test_id = test
	#get mocked kid !
	return 2

def get_nb_step(test) :
	#return the number of step required on a test
	return 6

def get_nb_step_user(test,user) :
	#return the number of step required on a test
	conn = sqlite3.connect('databases/'+str(test)+'.db')
	c = conn.cursor()
	c.execute("select count(*) from answer where user=\""+user+"\"")
	res = c.fetchall()
	conn.close()
	return res[0][0]

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
	nb = sampleList[0][5]
	for sample in sampleList :
		#check if user has not already processed this sample
		c.execute("select count(*) from answer where user=\""+user+"\" and syst_index=\""+sample[3]+"\"")
		#if it is the case then go to the next sample
		#then take the sample which has been processed the fewest time
		if sample[5] < nb :
			nb = sample[5]
			#keep the sample
			s = sample[1].split('/')
			s1 = "/test_sound/"+test+"/"+s[len(s)-1]
			s2 = "/test_sound/"+test+"/"+s[len(s)-1]
			samples = [{"id" : 1, "path" : s1},{"id" : 2, "path" : s2}]
	#s1 = "/test_sound/"+test+"/bird.wav"
	#s2 = "/test_sound/"+test+"/dolphin.wav"
	#samples = [{"id" : 1, "path" : s1},{"id" : 2, "path" : s2}]
	conn.close()
	return samples

def insert_data(test,data) :
	now = datetime.now()
	val = "\""+data["user"]+"\",\""+str(now)+"\",1,1,1";
	conn = sqlite3.connect('databases/'+str(test)+'.db')
	c = conn.cursor()
	c.execute("insert into answer(user,date,content,syst_index,question_index) values ("+val+")")
	conn.commit()
	conn.close()