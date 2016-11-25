controller_body = """
import model
import sys
import bottle
import sqlite3
import json
import os
import random
import config
from beaker.middleware import SessionMiddleware

bottle.debug(True)
app = bottle.Bottle()

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': False,
    'session.data_dir': './data',
    'session.auto': True
}


app_middlware = SessionMiddleware(app, session_opts)
app_session = bottle.request.environ.get('beaker.session')

@app.route('/login')
@app.post('/login')
def login():
	mail = post_get("email")
	app_session = bottle.request.environ.get('beaker.session')
	app_session['logged_in'] = True
	app_session['pseudo'] = mail
	bottle.redirect('/')

@app.route('/logout')
@app.post('/logout')
def logout():
	bottle.request.environ.get('beaker.session').delete()

@app.route('/login')
def toto():
	app_session = bottle.request.environ.get('beaker.session')
	if('pseudo' in app_session) :
		return "<p>You are already logged, please logout <a href=\"http://localhost:8080/logout\">here</a></p>"
	return bottle.template('login_form')

#bottle post methods
def postd():
	return bottle.request.forms


def post_get(name, default=''):
	return bottle.request.POST.get(name, default).strip()

def testLogin():
    app_session = bottle.request.environ.get('beaker.session')
    if 'pseudo' in app_session:
        return True
    else:
        return False


#home page
@app.route('/')
def home():
	return "<p>Hi! Welcome on our test plateform, if you want to get a free example, please go <a href=\"http://localhost:8080/test/1\">Here</a>!</p>"


@app.route('/test/:test')
def process_test(test):
	app_session = bottle.request.environ.get('beaker.session')
	#the following lines are to be uncommented later
	if not testLogin() :
		bottle.redirect('/login')
	user = app_session['pseudo']
	if not os.path.exists('databases/'+test+'.db') :
		return "<p>This test is not valid!! (no database linked)</p>"
	#proceed to the test
	#check if the test isn't finished yet
	if model.get_nb_step_user(test,user) < model.get_nb_step(test) :
		#proceed to a new step
		nbq = model.get_nb_questions(test)
		keys =[]
		for i in range(nbq) :
			keys.append(random.randint(0,1))
		(samples,index) = model.get_test_sample(test,user)
		systems = model.get_systems(test)
		data={"author":model.get_author(test),"description": model.get_description(test),"test_code":test,"samples" : samples, "systems": systems, "index": index}
		return bottle.template(test,data)
	else :
		return "<p>You have already done this test</p>"

@app.post('/test/:test')
def process_test_post(test):
	app_session = bottle.request.environ.get('beaker.session')
	#the following lines are to be uncommented later
	if not testLogin() :
		bottle.redirect('/login')
	user = app_session['pseudo']
	if not os.path.exists('databases/'+test+'.db') :
		return "<p>This test is not valid!! (no database linked)</p>"
	#get the post data and insert into db
	answers=[]
	i=1
	while post_get("question"+str(i))!="" :
	#for i in range(1,int(nb)+1) :
		answers.append({"index": i, "content": post_get("question"+str(i))})
		i=i+1
	post_data = {"author":model.get_author(test),"description": model.get_description(test),user":user,"answers": answers,"index": post_get("ref")}
	model.insert_data(test,post_data)
	#check if the test isn't finished yet
	if model.get_nb_step_user(test,user) < model.get_nb_step(test) :
		#proceed to a new step
		systems = model.get_systems(test)
		nbq = model.get_nb_questions(test)
		keys =[]
		for i in range(nbq) :
			keys.append(random.randint(0,1))
		(samples,index) = model.get_test_sample(test,user)
		data={"test_code":test, "samples" : samples, "systems": systems, "random_keys": keys, "index": index}
		return bottle.template(test,data)
	else :
		return "<p>Test finished thank you for your cooperation</p>"


#access to local static sound files
@app.route('/test_sound/:test/:filename#.*#')
def send_static(test, filename):
	return bottle.static_file(filename, root="./sound/%s/" % test)

#access to local static files
@app.route('/static/:type/:filename#.*#')
def send_static(type, filename):
	if type in ['css', 'js', 'img', 'fonts']:
		return bottle.static_file(filename, root="./static/%s/" % type)
	else:
		bottle.abort(404, "File not found")

def main():
	application = app
	bottle.run(app_middlware, host='localhost', port=8080)

if __name__ == "__main__":
	main()
"""

model_body="""
import sqlite3
from datetime import date, datetime
import random
import config

def get_nb_system() :
	#return the number of sample for a test!
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	c.execute("select count(*) from system")
	res = c.fetchall()
	conn.close()
	return int(res[0][0])

def get_nb_questions() :
	return config.nb_questions

def get_author():
	#get it from config.py
	return config.author

"name": "Test AB pour validation du XML",
"author": "Damien",
"nbInstances": "6",
"nbSteps": "10",
"nbConsistencySteps": "2",
"nbIntroductionSteps": "1",
"description": "Test AB",
"start": "2012-01-31",
"end": "2014-12-31",
"fixedPosition": "True"

def get_description():
	#get it from config.py
	return config.description

def get_name():
	#get it from config.py
	return config.name

def get_systems(test) :
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	c.execute("select id from system")
	res = c.fetchall()
	conn.close()
	res2=[]
	for r in res :
		res2.append(r[0])
	return res2

def get_nb_sample_by_system() :
	#return the number of samples of each system
	#get it from config.py
	return config.nb_sample_by_system

def get_nb_step() :
	#return the number of step required on a test
	#get it from config.py
	return config.nb_step

def get_nb_step_user(test,user) :
	#return the number of step made by a user on the test
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	c.execute("select count(*) from answer where user=\""+user+"\"")
	res = c.fetchall()
	conn.close()
	#return int(res[0][0])
	return 0

def get_metadata(test) :
	#get it from config.py
	return "mocked result"

def get_test_sample(test,user) :
	#load a tuple of sample depending of the user and the number of time processed
	nbSa = get_nb_sample_by_system(test)
	nbSy = get_nb_system(test)
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	c.execute("select * from sample")
	sampleList = c.fetchall()
	index=-1
	i=0
	nb=0
	stop = False
	samples=[]
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
				samples.append(s1)
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
				samples.append(s1)
		i=i+1
	conn.close()
	return (samples,index)


def insert_data(test,data) :
	now = datetime.now()
	conn = sqlite3.connect('data.db')
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
"""
testDirectory = "./tests/test1/"

def create_controller():
	print("|---------------------|")
	print("| controller creation |")
	print("v---------------------v")
	fo = open(testDirectory+"plateform.py", "wb")
	fo.write(controller_body)
	fo.close()
	print "Done.\n\n"

def create_model():
	print("|---------------------|")
	print("|   model creation    |")
	print("v---------------------v")
	fo = open(testDirectory+"model.py", "wb")
	fo.write(controller_body)
	fo.close()
	print "Done\n\n"

def main():
	create_controller()
	create_model()

if __name__ == "__main__":
	main()