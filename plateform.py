import model
import sys
import bottle
import sqlite3
import json
import os
from beaker.middleware import SessionMiddleware

bottle.debug(True)
app = bottle.Bottle()

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
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
	return "<p>Welcome!</p>"

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
		samples = model.get_test_sample(test,user)
		data={"test_code":test,"samples" : samples, "system": 1, "index": 1}
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
	nb=model.get_nb_question(test)
	answers=[]
	for i in range(1,nb+1) :
		answers.append(post_get("question"+str(i)))
	post_data = {"user":user,"answers": answers}
	model.insert_data(test,post_data)
	#check if the test isn't finished yet
	if model.get_nb_step_user(test,user) < model.get_nb_step(test) :
		#proceed to a new step
		samples = model.get_test_sample(test,user)
		data={"test_code":test, "samples" : samples, "system": 1, "index": 1}
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