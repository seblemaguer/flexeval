import sqlite3
from datetime import date, datetime
import random

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
	return int(res[0][0])

def get_author(test):
	conn = sqlite3.connect('databases/static_db.db')
	c = conn.cursor()
	c.execute("select author from test where id="+str(test))
	res = c.fetchall()
	conn.close()
	return res[0][0]

def get_description(test):
	conn = sqlite3.connect('databases/static_db.db')
	c = conn.cursor()
	c.execute("select description from test where id="+str(test))
	res = c.fetchall()
	conn.close()
	return res[0][0]

def get_name(test):
	conn = sqlite3.connect('databases/static_db.db')
	c = conn.cursor()
	c.execute("select name from test where id="+str(test))
	res = c.fetchall()
	conn.close()
	return res[0][0]

def get_systems(test) :
	conn = sqlite3.connect('databases/'+str(test)+'.db')
	c = conn.cursor()
	c.execute("select id from system")
	res = c.fetchall()
	conn.close()
	res2=[]
	for r in res :
		res2.append(r[0])
	return res2

def get_nb_question(test) :
	#return the number of sample for a test, query to make !
	conn = sqlite3.connect('databases/static_db.db')
	c = conn.cursor()
	c.execute("select nbInstances from test where id="+str(test))
	res = c.fetchall()
	conn.close()
	return int(res[0][0])

def get_nb_sample_by_system(test) :
	#return the number of samples of each system
	total=0
	conn = sqlite3.connect('databases/static_db.db')
	c = conn.cursor()
	c.execute("select nbSteps,nbConsistencySteps,nbIntroductionSteps,nbIntroductionSteps from test where id="+str(test))
	res = c.fetchall()
	conn.close()
	return int(res[0][0])+int(res[0][1])+int(res[0][2])

def get_nb_step(test) :
	#return the number of step required on a test
	conn = sqlite3.connect('databases/static_db.db')
	c = conn.cursor()
	c.execute("select nbInstances from test")
	res = c.fetchall()
	conn.close()
	return int(res[0][0])

def get_nb_step_user(test,user) :
	#return the number of step made by a user on the test
	conn = sqlite3.connect('databases/'+str(test)+'.db')
	c = conn.cursor()
	c.execute("select count(*) from answer where user=\""+user+"\"")
	res = c.fetchall()
	conn.close()
	#return int(res[0][0])
	return 0

def get_metadata(test) :
	conn = sqlite3.connect('databases/static_db.db')
	c = conn.cursor()
	c.execute("select * from test where id="+str(test))
	res = c.fetchall()
	conn.close()
	return res[0]

def get_test_sample(test,user) :
	#load a tuple of sample depending of the user and the number of time processed
	nbSa = get_nb_sample_by_system(test)
	nbSy = get_nb_system(test)
	conn = sqlite3.connect('databases/'+str(test)+'.db')
	c = conn.cursor()
	c.execute("select * from sample")
	sampleList = c.fetchall()
	index=-1
	i=0
	nb=0
	stop = False
	samples=[]
	sysL = get_systems(test)
	while not stop and i<len(sampleList)/2 :
		#check if user has not already processed this sample
		c.execute("select count(*) from answer where user=\""+user+"\" and syst_index=\""+str(sampleList[i][4])+"\"")
		b = c.fetchall()
		#print b[0][0]
		if b[0][0]==0 :
			index = i+1
			stop = True
			nb=sampleList[i][5]
			samples=[]
			#keep the sample
			for j in range(nbSy) :
				s = sampleList[i+j*nbSa][1].split('/')
				s1 = "/test_sound/"+test+"/"+s[len(s)-1]
				ra = random.randint(0,1)
				if ra==1 :
					samples.append(s1)
				else :
					samples.insert(0,s1)
		i=i+1
	#we have the first unprocessed step
	#now check if there is another test which have been processed less times
	#we start from where we finished previous loop
	while i < len(sampleList)/2 :
		#check if user has not already processed this sample
		c.execute("select count(*) from answer where user=\""+user+"\" and syst_index=\""+str(sampleList[i][4])+"\"")
		b = c.fetchall()
		if b[0][0]==0 and sampleList[i][5]<nb:
			nb = sampleList[i][5]
			index = i+1
			stop = True
			samples=[]
			#keep the sample
			for j in range(nbSy) :
				s = sampleList[i+j*nbSa][1].split('/')
				s1 = "/test_sound/"+test+"/"+s[len(s)-1]
				ra = random.randint(0,1)
				if ra==1 :
					samples.append(s1)
				else :
					samples.insert(0,s1)
		i=i+1
	conn.close()
	return (samples,index,systems)


def insert_data(test,data) :
	now = datetime.now()
	conn = sqlite3.connect('databases/'+str(test)+'.db')
	c = conn.cursor()
	answers = data["answers"]
	for answer in answers :
		val = (data["user"],str(now),answer["content"],data["index"],answer["index"])
		c.execute("insert into answer(user,date,content,syst_index,question_index) values (?,?,?,?,?)",val)
	#update the number of time processed for the sapmles
	c.execute("select nb_processed from sample where syst_index="+str(data["index"]))
	n = c.fetchall()[0][0]
	c.execute("update sample set nb_processed="+str(n+1)+" where syst_index="+str(data["index"]))
	conn.commit()
	conn.close()