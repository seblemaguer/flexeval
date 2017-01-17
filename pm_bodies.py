platform_body = """
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import model
import bottle
from bottle import request
import sqlite3
import json
import random
import config
from beaker.middleware import SessionMiddleware

bottle.debug(True)

views_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views/')
bottle.TEMPLATE_PATH.insert(0, views_path)
#bottle.TEMPLATE_PATH.insert(0,os.path.dirname(os.path.abspath(__file__)))
app = bottle.Bottle()

# TO MODIFY DEPENDING ON DEPLOYMENT CONFIGURATION
# example: '/mytest'
# DO NOT FORGET TO PUT HEADING /
app.config['myapp.APP_PREFIX'] = '' 

session_opts = {
	'session.type': 'file',
	'session.cookie_expires': False,
	'session.data_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)),'data'),
	'session.auto': True
}

app_middlware = SessionMiddleware(app, session_opts)
app_session = bottle.request.environ.get('beaker.session')

@app.route('/')
def badroute():
	data={"APP_PREFIX":request.app.config['myapp.APP_PREFIX'], "name":model.get_name(), "author":model.get_author(), "description":model.get_description(), "welcomeText":model.get_welcome_text()}
	return bottle.template('index', data)

@app.route('/login')
@app.post('/login')
def login():
	mail = post_get("email")
	app_session = bottle.request.environ.get('beaker.session')
	app_session['logged_in'] = True
	app_session['pseudo'] = mail
	bottle.redirect(request.app.config['myapp.APP_PREFIX']+'/test')

@app.route('/logout')
@app.post('/logout')
def logout():
	bottle.request.environ.get('beaker.session').delete()
	bottle.redirect(request.app.config['myapp.APP_PREFIX']+'/')

@app.route('/login')
def toto():
	app_session = bottle.request.environ.get('beaker.session')
	if('pseudo' in app_session) :
		return "<p>You are already logged, please logout <a href='"+request.app.config['myapp.APP_PREFIX']+"/logout'>here</a></p>"
	data={"APP_PREFIX":request.app.config['myapp.APP_PREFIX'], "name":model.get_name(), "author":model.get_author(), "description":model.get_description(), "welcomeText":model.get_welcome_text()}
	return bottle.template('index', data)

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

@app.route('/test')
def process_test():
	app_session = bottle.request.environ.get('beaker.session')
	#the following lines are to be uncommented later
	if not testLogin() :
		bottle.redirect(request.app.config['myapp.APP_PREFIX']+'/login')
	user = app_session['pseudo']
	#proceed to the test
	#check if the test isn't finished yet
	if model.get_nb_step_user(user) < model.get_nb_step() :
		#proceed to a new step
		if int(config.nbIntroductionSteps) > 0 and model.get_nb_step_user(user) == 0 and not 'intro_done' in app_session:
			if not 'nb_intro_passed' in app_session:
				app_session['nb_intro_passed'] = 0
			(samples, systems, index) = model.get_intro_sample(user)
			data={"APP_PREFIX":request.app.config['myapp.APP_PREFIX'], "name":model.get_name(), "author":model.get_author(), "description":model.get_description(), "samples":samples, "systems":systems, "nfixed": model.get_nb_position_fixed(), "index":index, "user":user, "introduction": True, "step": int(model.get_nb_step_user(user)+1), "totalstep" : model.get_nb_step(), "progress" : model.get_progress(user)}
		else:
			(samples, systems, index) = model.get_test_sample(user)
			data={"APP_PREFIX":request.app.config['myapp.APP_PREFIX'], "name":model.get_name(), "author":model.get_author(), "description":model.get_description(), "samples":samples, "systems":systems, "nfixed": model.get_nb_position_fixed(), "index":index, "user":user, "step": int(model.get_nb_step_user(user)+1), "totalstep" : model.get_nb_step(), "progress" : model.get_progress(user)}
		return bottle.template('template', data)
	else :
		bottle.request.environ.get('beaker.session').delete()
		return "<p>You have already done this test</p>"

@app.post('/test')
def process_test_post():
	app_session = bottle.request.environ.get('beaker.session')
	#the following lines are to be uncommented later
	if not testLogin() :
		bottle.redirect(request.app.config['myapp.APP_PREFIX']+'/login')
	user = app_session['pseudo']
	#get the post data and insert into db
	if ('intro_done' in app_session and app_session['intro_done'] == True) or int(config.nbIntroductionSteps) <= 0:
		systems=[]
		i=1
		while post_get("system"+str(i))!="" :
			systems.append(post_get("system"+str(i)))
			i=i+1
		answers=[]
		i=1
		while post_get("question"+str(i))!="" :
			ct = post_get("question"+str(i)).split(";;")
			if len(ct)==1:
				answers.append({"index": i, "content": ct[0]})
			else :
				answers.append({"index": i, "content": ct[0], "target": ct[1]})
			i=i+1
		post_data = {"author":model.get_author(),"user":user,"answers": answers,"systems": systems,"index": post_get("ref")}
		model.insert_data(post_data)
	else:
		app_session['nb_intro_passed'] += 1
		if (app_session['nb_intro_passed'] >= int(config.nbIntroductionSteps)):
			app_session['intro_done'] = True
	#check if the test isn't finished yet
	if model.get_nb_step_user(user) < model.get_nb_step() :
		bottle.redirect(request.app.config['myapp.APP_PREFIX']+'/test')
	else :
		data={"APP_PREFIX":request.app.config['myapp.APP_PREFIX'], "name":model.get_name(), "author":model.get_author(), "description":model.get_description(), "welcomeText":model.get_welcome_text()}
		bottle.request.environ.get('beaker.session').delete()
		return bottle.template('completed', data)
		#return "<p>Test finished thank you for your cooperation</p>"

#access to local static files
@app.route('/static/:type/:filename#.*#')
def send_static(type, filename):
	return bottle.static_file(filename, root=os.path.join(os.path.dirname(os.path.abspath(__file__)),"static/%s/") % type)

#access to local static sound files
@app.route('/media/:media/:syst/:filename#.*#')
@app.route('/media/:media/./:syst/:filename#.*#')
def send_static(media, syst, filename):
	return bottle.static_file(filename, root=os.path.join(os.path.dirname(os.path.abspath(__file__)),"media/%s/") % media+"/"+syst)

@app.route(':badroute')
def badroute(badroute):
	bottle.redirect(request.app.config['myapp.APP_PREFIX']+'/test')

def main():
	bottle.run(app_middlware, host='localhost', port=8080, server='paste')

if __name__ == "__main__":
	main()
else:
	application = app_middlware
"""


model_body="""import os
import sqlite3
from datetime import date, datetime
import random
import config
import itertools
import operator

def get_nb_system() :
	#return the number of sample for a test!
	conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data.db'))
	c = conn.cursor()
	c.execute("select count(*) from system")
	res = c.fetchall()
	conn.close()
	return int(res[0][0])

def get_nb_position_fixed():
	return int(config.nbFixedPosition)

def get_nb_system_display() :
	return int(config.nbSystemDisplayed)

def get_nb_questions() :
	return int(config.nbQuestions)

def get_author():
	#get it from config.py
	return config.author
	
def get_questions_type():
	#get the text of questions as an array
	return config.questionsType

def get_description():
	#get it from config.py
	return config.description

def get_welcome_text():
	#get it from config.py
	return config.welcomeText

def get_name():
	#get it from config.py
	return config.name

def get_nb_sample_by_system() :
	#return the number of samples of each system
	#get it from config.py
	return int(config.nbSampleBySystem)

def get_nb_step() :
	#return the number of step required on a test
	#get it from config.py
	return int(config.nbSteps)

def get_nb_step_user(user) :
	#return the number of step made by a user on the test
	conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data.db'))
	c = conn.cursor()
	c.execute('select count(*) from answer where user="'+user+'"')
	res = c.fetchall()
	conn.close()
	nbans = res[0][0]
	return int(nbans/get_nb_questions())

def get_progress(user):
	# return the ratio of steps achieved by the user over the total number of steps
	return 100*get_nb_step_user(user)/get_nb_step()

def get_metadata() :
	#get it from config.py
	metadata=dict()
	for i in dir(config):
		#i,"  ",getattr(config,i)
		b = re.search(r'__.+__',str(i))
		if not b:
			metadata[str(i)]=getattr(config,i)
	return metadata

def get_shuffled_list_of_system_ids(nbFixed, connection) :
	# Build the list of system IDs such that fixed position systems are returned in priority,
	# then systems with lowest number of answers in priority.
	
	# Get system IDs
	connection.execute('select id_system, sum(nb_processed) as nb_answers from sample group by id_system order by id asc')
	ids = connection.fetchall()
	# Keep fixed systems aside
	fixed_ids = []
	if nbFixed > 0:
		fixed_ids = ids[0:nbFixed]
		ids = ids[nbFixed:]
	# Sort remaining IDs according to number of answers
	ids = sorted(ids, key=lambda line: int(line[1]))
	# Let m the minimum number of answers
	# Shuffle all systems with number of answers ranging between m and m+delta
	m = ids[0][1]
	delta = 1
	low_votes_ids = list(filter(lambda line: line[1] <= m+delta, ids))
	random.shuffle(low_votes_ids)
	# and append others
	higher_votes_ids = list(filter(lambda line: line[1] > m+delta, ids))
	# Shuffle all systems with similar number of answers
	def gather_similar_systems(l):
		it = itertools.groupby(l, operator.itemgetter(1))
		for key, subiter in it:
			yield list(subiter)
	shuffled_higher_votes_ids = []
	for group in gather_similar_systems(higher_votes_ids):
		random.shuffle(group)
		shuffled_higher_votes_ids += group
	
	return [line[0] for line in fixed_ids+low_votes_ids+shuffled_higher_votes_ids];

def get_test_sample(user) :
	random.seed()
	nbToKeep = int(config.nbSystemDisplayed)
	dir = os.path.dirname(os.path.abspath(__file__))
	conn = sqlite3.connect(os.path.join(dir,'data.db'))
	c = conn.cursor()
	c.execute("select syst_index, sum(nb_processed) from sample where type='test' group by syst_index")
	res= c.fetchall()
	validlist=[]
	min=0
	for r in res :
		#check if user have already done it
		c.execute('select count(*) from answer where user="'+user+'" and syst_index='+str(r[0]))
		nb = c.fetchall()
		if nb[0][0] ==0:
			if validlist==[]:
				min = r[1]
			if r[1] < min :
				min = r[1]
				validlist=[r]
			elif r[1]==min:
				validlist.append(r)
	index = validlist[random.randint(0,len(validlist)-1)][0]
	samples=[]
	systems=[]
	
	n = get_nb_position_fixed()
	
	shuffled_ids = get_shuffled_list_of_system_ids(n, c)
	
	c.execute('select nb_processed, id_system, path from sample where syst_index='+str(index)+' order by nb_processed asc')
	systs = {}
	for s in c.fetchall():
		systs[s[1]] = s
	
	i=0
	
	while i<nbToKeep :
		systems.append(shuffled_ids[i])
		if config.useMedia=='True' :
			samples.append('media/'+systs[shuffled_ids[i][0]][2])
		else :
			samples.append(systs[shuffled_ids[i]][2])
		i=i+1
	
	if n<=0:
		r = random.random()
		random.shuffle(samples, lambda: r)
		random.shuffle(systems, lambda: r)
	elif n>=get_nb_system_display(): #'False' to false ?
		pass
	else :
		sa1 = samples[0:n]
		sa2 = samples[n:]
		sy1 = systems[0:n]
		sy2 = systems[n:]
		r = random.random()
		random.shuffle(sa2, lambda: r)
		random.shuffle(sy2, lambda: r)
		sa1.extend(sa2)
		samples=sa1
		sy1.extend(sy2)
		systems=sy1
	
	conn.close()
	return (samples, systems, index)

def get_intro_sample(user) :
	random.seed()
	nbToKeep = int(config.nbSystemDisplayed)
	dir = os.path.dirname(os.path.abspath(__file__))
	conn = sqlite3.connect(os.path.join(dir,'data.db'))
	c = conn.cursor()
	c.execute("select syst_index from sample where type='intro' group by syst_index")
	res= c.fetchall()
	index= res[0][0]
	for r in res :
		c.execute('select count(*) from answer where user="'+user+'" and syst_index='+str(r[0]))
		nb = c.fetchall()
		if nb[0][0] ==0:
			index = r[0]
	samples=[]
	systems=[]
	
	n = get_nb_position_fixed()
	
	shuffled_ids = get_shuffled_list_of_system_ids(n, c)
	
	c.execute('select nb_processed, id_system, path from sample where syst_index='+str(index)+' order by nb_processed asc')
	systs = c.fetchall()
	
	i=0
	while i<nbToKeep :
		systems.append(systs[i][1])
		if config.useMedia=='True' :
			samples.append('media/'+systs[i][2])
		else :
			samples.append(systs[i][2])
		i=i+1

	if n<=0:
		r = random.random()
		random.shuffle(samples, lambda: r)
		random.shuffle(systems, lambda: r)
	elif n>=get_nb_system_display(): #'False' to false ?
		pass
	else :
		sa1 = samples[0:n]
		sa2 = samples[n:]
		sy1 = systems[0:n]
		sy2 = systems[n:]
		r = random.random()
		random.shuffle(sa2, lambda: r)
		random.shuffle(sy2, lambda: r)
		sa1.extend(sa2)
		samples=sa1
		sy1.extend(sy2)
		systems=sy1
	conn.close()
	return (samples, systems, index)


def insert_data(data) :
	now = datetime.now()
	conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data.db'))
	c = conn.cursor()
	answers = data['answers']
	for answer in answers :
		#val = (data['user'],str(now),answer['content'],data['index'],answer['index'])
		#c.execute('insert into answer(user,date,content,syst_index,question_index) values (?,?,?,?,?)',val)
		sysval=""
		systs=""
		for i in range(int(config.nbSystemDisplayed)):
			sysval=sysval+"\\""+data['systems'][i]+"\\""
			systs=systs+"system"+str(i+1)
			if(i<int(config.nbSystemDisplayed)-1):
				sysval=sysval+","
				systs=systs+","
		
		if "target" in answer :
			val = "\\""+str(data['user'])+"\\",\\""+str(now)+"\\",\\""+answer['content']+"\\",\\""+str(data['index'])+"\\",\\""+str(answer['index'])+"\\",\\""+answer["target"]+"\\","+sysval
			conn.execute("insert into answer(user,date,content,syst_index,question_index,content_target,"+systs+") values ("+val+")")
		else :
			val = "\\""+str(data['user'])+"\\",\\""+str(now)+"\\",\\""+answer['content']+"\\",\\""+str(data['index'])+"\\",\\""+str(answer['index'])+"\\","+sysval
			conn.execute("insert into answer(user,date,content,syst_index,question_index,"+systs+") values ("+val+")")
		
		#update the number of time processed for the samples
		c.execute('select nb_processed from sample where id_system="'+answer['target']+'" and syst_index='+str(data['index']))
		n = c.fetchall()[0][0]
		conn.execute('update sample set nb_processed='+str(n+1)+' where id_system="'+answer['target']+'" and syst_index='+str(data['index']))
		conn.commit()
	#update the number of time processed for the samples
	#c.execute('select nb_processed from sample where syst_index='+str(data['index']))
	#n = c.fetchall()[0][0]
	#conn.execute('update sample set nb_processed='+str(n+1)+' where syst_index='+str(data['index']))
	#conn.commit()
	conn.close()
"""
