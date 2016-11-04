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

@app.post('/login')
def login():
	mail = post_get("email")
	app_session = bottle.request.environ.get('beaker.session')
	app_session['logged_in'] = True
	app_session['pseudo'] = mail
	return "<p>Welcome!</p>"

@app.post('/logout')
def logout():
	bottle.request.environ.get('beaker.session')['pseudo'] = None
	redirect('/login')

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
	return "<p>Nothing to see here!</p>"


@app.route('/test/:test')
def process_test(test):
	app_session = bottle.request.environ.get('beaker.session')
	if testLogin():
		redirect('/login')
	if not os.path.exists('databases/'+test+'.db') :
		return "<p>This test is not valid!! (no database linked)</p>"
	conn = sqlite3.connect('databases/'+test+'.db')
	c = conn.cursor()
	#load all the sample, see later for a strategic uses
	c.execute("select * from sample")
	sampleContent = c.fetchall()
	conn.close()
	s1 = "/test_sound/"+test+"/bird.wav"
	s2 = "/test_sound/"+test+"/dolphin.wav"
	samples = [{"id" : 1, "path" : s1},{"id" : 2, "path" : s2}]
	
	data={"test_code":test,"sample_content":str(sampleContent),"samples" : samples}
	return bottle.template(test,data)

@app.post('/test/:test')
def process_test_post(test):
	app_session = bottle.request.environ.get('beaker.session')
	if testLogin():
		redirect('/login')
	conn = sqlite3.connect('databases/'+test+'.db')

	s = post_get("sample1")
	if post_get("sample2") != "":
		s = samples +","+post_get("sample2")
	if post_get("sample3") != "":
		s = samples +","+post_get("sample3")
	c = conn.cursor()
	#insert the answer first
	#c.execute("insert into answer (type_qestion,date,sample1,sample2,sample3) values(\"AB\",CURRENT_TIMESTAMP,"+s+")")
	#load all the sample, see later for a strategic uses
	c.execute("select * from sample")
	sampleContent = c.fetchall()
	#c.commit()
	conn.close()
	s1 = "/test_sound/"+test+"/bird.wav"
	s2 = "/test_sound/"+test+"/dolphin.wav"
	samples = [{"id" : 1, "path" : s1},{"id" : 2, "path" : s2}]
	data={"test_code":test,"sample_content":str(sampleContent),"samples" : samples}
	return bottle.template(test,data)


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