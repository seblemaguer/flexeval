plateform_body = """
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

views_path = os.path.join(os.path.dirname(__file__), 'views/')
bottle.TEMPLATE_PATH.insert(0, views_path)
#bottle.TEMPLATE_PATH.insert(0,os.path.dirname(__file__))
app = bottle.Bottle()

session_opts = {
	'session.type': 'file',
	'session.cookie_expires': False,
	'session.data_dir': os.path.join(os.path.dirname(__file__),'data'),
	'session.auto': True
}

app_middlware = SessionMiddleware(app, session_opts)
app_session = bottle.request.environ.get('beaker.session')

@app.route('/')
def badroute():
	data={"name":model.get_name(), "author":model.get_author(), "description":model.get_description(), "welcomeText":model.get_welcome_text()}
	return bottle.template('index', data)

@app.route('/login')
@app.post('/login')
def login():
	mail = post_get("email")
	app_session = bottle.request.environ.get('beaker.session')
	app_session['logged_in'] = True
	app_session['pseudo'] = mail
	bottle.redirect('/test')

@app.route('/logout')
@app.post('/logout')
def logout():
	bottle.request.environ.get('beaker.session').delete()
	bottle.redirect('/')

@app.route('/login')
def toto():
	app_session = bottle.request.environ.get('beaker.session')
	if('pseudo' in app_session) :
		return "<p>You are already logged, please logout <a href='http://localhost:8080/logout'>here</a></p>"
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

@app.route('/test')
def process_test():
	app_session = bottle.request.environ.get('beaker.session')
	#the following lines are to be uncommented later
	if not testLogin() :
		bottle.redirect('/login')
	user = app_session['pseudo']
	#proceed to the test
	#check if the test isn't finished yet
	if model.get_nb_step_user(user) < model.get_nb_step() :
		#proceed to a new step
		nbq = model.get_nb_questions()
		keys = []
		for i in range(nbq) :
			keys.append(random.randint(0,1))
		if model.get_nb_step_user(user) == 0 and not 'intro_done' in app_session:
			if not 'nb_intro_passed' in app_session:
				app_session['nb_intro_passed'] = 1
			else :
				app_session['nb_intro_passed'] += 1
			if (app_session['nb_intro_passed'] >= int(config.nbIntroductionSteps)):
				app_session['intro_done'] = False
			(samples, systems, index) = model.get_intro_sample(user)
		else:
			app_session['intro_done'] = True
			(samples, systems, index) = model.get_test_sample(user)
		data={"name":model.get_name(), "author":model.get_author(), "description":model.get_description(), "samples":samples, "systems":systems, "index":index, "user":user}
		return bottle.template('template', data)
	else :
		return "<p>You have already done this test</p>"

@app.post('/test')
def process_test_post():
	app_session = bottle.request.environ.get('beaker.session')
	#the following lines are to be uncommented later
	if not testLogin() :
		bottle.redirect('/login')
	user = app_session['pseudo']
	#get the post data and insert into db
	if 'intro_done' in app_session and app_session['intro_done'] == True:
		systems=[]
		i=1
		while post_get("system"+str(i))!="" :
			systems.append(post_get("system"+str(i)))
			i=i+1
		answers=[]
		i=1
		while post_get("question"+str(i))!="" :
			answers.append({"index": i, "content": post_get("question"+str(i))})
			i=i+1
		post_data = {"author":model.get_author(),"user":user,"answers": answers,"systems": systems,"index": post_get("ref")}
		model.insert_data(post_data)
	#check if the test isn't finished yet
	if model.get_nb_step_user(user) < model.get_nb_step() :
		bottle.redirect('/test')
	else :
		return "<p>Test finished thank you for your cooperation</p>"

#access to local static files
@app.route('/static/:type/:filename#.*#')
def send_static(type, filename):
	return bottle.static_file(filename, root=os.path.join(os.path.dirname(__file__),"static/%s/") % type)

#access to local static sound files
@app.route('/media/:media/:syst/:filename#.*#')
@app.route('/media/:media/./:syst/:filename#.*#')
def send_static(media, syst, filename):
	return bottle.static_file(filename, root=os.path.join(os.path.dirname(__file__),"media/%s/") % media+"/"+syst)

@app.route('/:badroute')
def badroute(badroute):
	bottle.redirect('/test')

def main():
	application = app
	bottle.run(app_middlware, host='localhost', port=8080)

if __name__ == "__main__":
	main()
"""


model_body="""
import os
import sqlite3
from datetime import date, datetime
import random
import config

def get_nb_system() :
	#return the number of sample for a test!
	conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),'data.db'))
	c = conn.cursor()
	c.execute("select count(*) from system")
	res = c.fetchall()
	conn.close()
	return int(res[0][0])

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
	return int(config.nbInstances)

def get_nb_step_user(user) :
	#return the number of step made by a user on the test
	conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),'data.db'))
	c = conn.cursor()
	c.execute('select count(*) from answer where user="'+user+'"')
	res = c.fetchall()
	conn.close()
	nbans = res[0][0]
	return nbans/get_nb_questions()

def get_metadata() :
	#get it from config.py
	metadata=dict()
	for i in dir(config):
		#i,"  ",getattr(config,i)
		b = re.search(r'__.+__',str(i))
		if not b:
			metadata[str(i)]=getattr(config,i)
	return metadata

def get_test_sample(user) :
	nbToKeep = int(config.nbSystemDisplayed)
	dir = os.path.dirname(__file__)
	conn = sqlite3.connect(os.path.join(dir,'data.db'))
	c = conn.cursor()
	c.execute("select syst_index, sum(nb_processed) from sample where type='test' group by syst_index")
	res= c.fetchall()
	index= res[0][0]
	mini = res[0][1]
	for r in res :
		if r[1]<mini :
			#check if user have already done it
			c.execute('select count(*) from answer where user="'+user+'" and syst_index='+str(r[0]))
			nb = c.fetchall()
			if nb[0][0] ==0:
				index = r[0]
				mini = r[1]
	samples=[]
	systems=[]
	c.execute('select nb_processed, id_system, path from sample where syst_index='+str(index)+' order by nb_processed asc')
	systs = c.fetchall()
	i=0
	while i<nbToKeep :
		systems.append(systs[i][1])
		samples.append('media/'+systs[i][2])
		i=i+1
	conn.close()
	return (samples, systems, index)

def get_intro_sample(user) :
	nbToKeep = int(config.nbSystemDisplayed)
	dir = os.path.dirname(__file__)
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
	c.execute('select nb_processed, id_system, path from sample where syst_index='+str(index)+' order by nb_processed asc')
	systs = c.fetchall()
	i=0
	while i<nbToKeep :
		systems.append(systs[i][1])
		samples.append('media/'+systs[i][2])
		i=i+1
	if config.fixedPosition=='False': #'False' to false ?
		r = random.random()
		random.shuffle(samples, lambda: r)
		random.shuffle(systems, lambda: r)
	conn.close()
	return (samples, systems, index)

def insert_data(data) :
	now = datetime.now()
	conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),'data.db'))
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
			c.execute("insert into answer(user,date,content,syst_index,question_index,content_target,"+systs+") values ("+val+")")
		else :
			val = "\\""+str(data['user'])+"\\",\\""+str(now)+"\\",\\""+answer['content']+"\\",\\""+str(data['index'])+"\\",\\""+str(answer['index'])+"\\","+sysval
			c.execute("insert into answer(user,date,content,syst_index,question_index,"+systs+") values ("+val+")")
	#update the number of time processed for the samples
	c.execute('select nb_processed from sample where syst_index='+str(data['index']))
	n = c.fetchall()[0][0]
	c.execute('update sample set nb_processed='+str(n+1)+' where syst_index='+str(data['index']))
	conn.commit()
	conn.close()
"""


login_form="""
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="description" content="">
	<meta name="author" content="">

	<title>Subjective tests plateform - login</title>

	<!-- Bootstrap Core JavaScript -->
	<script src="/static/js/bootstrap.min.js"></script>
	<!-- Bootstrap Core CSS -->
	<link href="/static/css/bootstrap.min.css" rel="stylesheet">
</head>

<body>
	<div class="container">
		<div class="row">
			<div class="col-md-4 col-md-offset-4">
				<div class="login-panel panel panel-default">
					<div class="panel-heading">
						<h3 class="panel-title">Please Log In</h3>
					</div>
					<div class="panel-body">
						<form role="form" action="/login" method="POST">
							<fieldset>
								<div class="form-group">
									<input class="form-control" placeholder="E-mail" name="email" autofocus>
								</div>
								<!-- Change this to a button or input when using this as a form -->
								<input type="submit" class="btn btn-lg btn-success btn-block" value="Login">
							</fieldset>
						</form>
					</div>
				</div>
			</div>
		</div>
	</div>
</body>

</html>
"""


index_form="""
<!DOCTYPE html>
<html lang="en">

<head>

	<meta charset="utf-8">

	<title>Subjective tests plateform - {{name}}</title>

	<!-- Bootstrap Core CSS -->
	<link href="/static/css/bootstrap.min.css" rel="stylesheet">
	<link href="/static/css/tests.css" rel="stylesheet">
	<link href="/static/css/jquery-ui.min.css" rel="stylesheet">
	<script src="/static/js/jquery.js"></script>
	<script src="/static/js/jquery-ui.min.js"></script>

</head>

<body>

	<div class="jumbotron">
		<img src="/static/img/logo.jpg" class="img-responsive pull-left" alt="logo">
		<div class="container">
			<div class="col-md-6 col-md-offset-3">
				<h1>{{name}}</h1><span>
				<h3>Made by {{author}}</h3>
				<p class="lead">{{description}}</p>
			</div>
		</div>
	</div>

	<div class="container">
		<p>{{welcomeText}}</p>
		<p>Veuillez cliquer <a href="/test">ICI</a> afin de commencer le test.</p>
	</div>

	</body>

</html>
"""