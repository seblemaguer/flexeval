#!/usr/bin/python

import csv
import bottle
import json
import os
import random
import re
import sqlite3
import sys
from bottle import request
from beaker.middleware import SessionMiddleware


sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import config
import model

bottle.debug(True)

views_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views/')
bottle.TEMPLATE_PATH.insert(0, views_path)
app = bottle.Bottle()

app.config['myapp.APP_PREFIX'] = model.get_prefix()

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
	book = model.get_book_variable_module_name('config')
	data={'APP_PREFIX':request.app.config['myapp.APP_PREFIX'], 'config': book}
	return bottle.template('index', data)

@app.post('/perso/lsf/commentaires')
def persolsfcommentaires():

	video = bottle.request.POST.get("video")
	model.generate_comment_table()
	model.add_comment_table(bottle.request.POST.get("courriel"),bottle.request.POST.get("commentaire"),video)


@app.get('/devtestfeedback')
def alaid():
	book = model.get_book_variable_module_name('config')
	data={'APP_PREFIX':request.app.config['myapp.APP_PREFIX'], 'config': book}
	return bottle.template('completed', data)


@app.route('/alreadyregister/<key>/<val>')
def async_rec_user_register_verification(key,val):
	res= model.already_in_user_table(key,val)
	return str(res)

@app.route('/login')

@app.route('/login')
@app.post('/login')
def login():
	mail = post_get('email')
	pattern='(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
	print(mail)
	if not re.match(pattern,mail) :
		book = model.get_book_variable_module_name('config')
		data={'APP_PREFIX':request.app.config['myapp.APP_PREFIX'], 'config': book, 'error' : 'Invalid email address'}
		return bottle.template('index', data)
	app_session = bottle.request.environ.get('beaker.session')
	app_session['logged_in'] = True
	app_session['pseudo'] = mail


	model.generate_user_table(request.forms.dict)
	model.populate_user_table(request.forms.dict,"email")

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
		return '<p>You are already logged, please logout <a href="'+request.app.config['myapp.APP_PREFIX']+'/logout">here</a></p>'
	book = model.get_book_variable_module_name('config')
	data={'APP_PREFIX':request.app.config['myapp.APP_PREFIX'], 'config': book}
	return bottle.template('index', data)

# Bottle post methods
def postd():
	return bottle.request.forms

def post_get(name, default=''):
	return bottle.request.POST.get(name, default).strip()

def get_question_answer_keys():
	keys = list()
	for k in bottle.request.POST:
		# If prefix is "answer" and the corresponding question exists
		prefix = re.compile('^answer(.*)')
		is_answer = prefix.match(k)
		if is_answer:
			suffix = is_answer.group(1)
			question = "question_index" + suffix
			# Add in the set of working keys
			if question in bottle.request.POST.keys():
				print(suffix)
				keys.append(suffix)
	return keys

def testLogin():
	app_session = bottle.request.environ.get('beaker.session')
	if 'pseudo' in app_session:
		return True
	else:
		return False

def encode_system(syst) :
	#proceede to the encoding of your system name here so it won't apear clearly in source code
	return str(syst)

def decode_system(syst) :
	#reverse operation of previous one
	return str(syst)

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
		book = model.get_book_variable_module_name('config')
		if model.get_nb_intro_steps() > 0 and model.get_nb_step_user(user) == 0 and not 'intro_done' in app_session:
			if not 'nb_intro_passed' in app_session:
				app_session['nb_intro_passed'] = 0
			(samples, systems, index) = model.get_intro_sample(user)
			enc_systems = []
			for s in systems :
				enc_systems.append(encode_system(s))
			hidden = '<input type="hidden" name="ref" value="'+str(index)+'">'
			j=0
			for s in enc_systems :
				hidden = hidden + '<input type="hidden" name="real_system_'+str(j)+'" value="'+s+'">'
				j=j+1
			data={"APP_PREFIX":request.app.config['myapp.APP_PREFIX'], "samples":samples, "systems":enc_systems, "nfixed": model.get_nb_position_fixed(), "index":index, "user":user, "introduction": True, "step": app_session['nb_intro_passed']+1, "totalstep" : model.get_nb_intro_steps(), "progress" : (100*(app_session['nb_intro_passed']+1))/model.get_nb_intro_steps(), "config": book, "hidden_fields": hidden}
		else:
			(samples, systems, index) = model.get_test_sample(user)
			enc_systems = []
			for s in systems :
				enc_systems.append(encode_system(s))
			hidden = '<input type="hidden" name="ref" value="'+str(index)+'">'
			j=1
			for s in enc_systems :
				hidden = hidden + '<input type="hidden" name="real_system_'+str(j)+'" value="'+s+'">'
				j=j+1
			book = model.get_book_variable_module_name('config')
			data={"APP_PREFIX":request.app.config['myapp.APP_PREFIX'], "samples":samples, "systems":enc_systems, "nfixed": model.get_nb_position_fixed(), "index":index, "user":user, "introduction": False, "step": model.get_nb_step_user(user)+1, "totalstep" : model.get_nb_step(), "progress" : model.get_progress(user), "config": book, "hidden_fields": hidden}
		return bottle.template('template', data)
	else :
                book = model.get_book_variable_module_name('config')
		data={"APP_PREFIX":request.app.config['myapp.APP_PREFIX'], "config": book, "already_completed": True}
		bottle.request.environ.get('beaker.session').delete()
		return bottle.template('completed', data)

@app.post('/test')
def process_test_post():
	process_answers()

@app.post('/answer')
def process_answers():
	app_session = bottle.request.environ.get('beaker.session')
	if not 'nb_intro_passed' in app_session:
		app_session['nb_intro_passed'] = 0
	if model.get_nb_intro_steps() == 0 and app_session['nb_intro_passed'] == 0:
		app_session['intro_done'] = True
	#the following lines are to be uncommented later
	if not testLogin() :
		bottle.redirect(request.app.config['myapp.APP_PREFIX']+'/login')
	user = app_session['pseudo']
	#get the post data and insert into db
	if ('intro_done' in app_session and app_session['intro_done'] == True) or model.get_nb_step_user(user) > 0:
		systems=[]
		keys = get_question_answer_keys()
		s=1
		while post_get("real_system_"+str(s))!="" :
			systems.append(post_get("real_system_"+str(s)))
			s=s+1
		answers=[]

		for k in keys:
			system_index = 1
			question_index = 1
			content = post_get("answer"+k)
			if "system_index"+k in bottle.request.POST:
				system_index = post_get("system_index"+k)
			if "question_index"+k in bottle.request.POST:
				question_index = post_get("question_index"+k)
			print({"system_index": system_index, "question_index": question_index, "content": content})
			answers.append({"system_index": system_index, "question_index": question_index, "content": content})
		post_data = {"author":model.get_author(),"user":user,"answers": answers,"systems": systems,"sample_index": post_get("ref")}
		model.insert_data(post_data)
	else:
		app_session['nb_intro_passed'] += 1
		if (app_session['nb_intro_passed'] >= model.get_nb_intro_steps()):
			app_session['intro_done'] = True
	#check if the test isn't finished yet
	if model.get_nb_step_user(user) < model.get_nb_step() :
		bottle.redirect(request.app.config['myapp.APP_PREFIX']+'/test')
	else :
		book = model.get_book_variable_module_name('config')
		data={"APP_PREFIX":request.app.config['myapp.APP_PREFIX'], "config": book, "already_completed": False}
		bottle.request.environ.get('beaker.session').delete()
		return bottle.template('completed', data)

@app.route('/export')
def export_db():
	book = model.get_book_variable_module_name('config')
	data={'APP_PREFIX':request.app.config['myapp.APP_PREFIX'], 'config': book}
	return bottle.template('export',data)

@app.post('/export')
def export_db_ok():
	if(post_get('token')==model.get_token()):
		if post_get('type') == "DB" :
			return bottle.static_file('data.db', root=os.path.dirname(os.path.abspath(__file__)),download='data.db')
		elif post_get('type') == "CSV" :
			#get the list of systems
			systems= []
			for i in range(1,model.get_nb_system_display()+1):
				systems.append('System num '+str(i))
			with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.csv'), 'w') as csvfile:
				fieldnames = ['user', 'date', 'content', 'system index', 'sample index', 'question index']
				fieldnames = fieldnames + systems
				writer = csv.DictWriter(csvfile, delimiter=";", fieldnames=fieldnames)
				writer.writeheader()
				#query the answers on the db from the model
				answers = model.get_answers()
				sys = model.get_systems()
				for a in answers :
					ct_value = ""
					if not a[4] is None:
							ct_value = sys[int(a[4])]
					content = ""
					if type(a[3]) is unicode:
						content = a[3].encode("utf8")
					else:
						content = a[3]
					row = {'user': a[1], 'date': a[2], 'content': content, 'system index': ct_value, 'sample index': a[5], 'question index': a[6]}
					# row = {'user': a[1], 'date': a[2], 'content': a[3], 'system index': ct_value, 'sample index': a[5], 'question index': a[6]}
					#'system1': sys[int(a[7])], 'system2': sys[int(a[8])], 'system3': sys[int(a[9])], 'system4': sys[int(a[10])], 'system5': sys[int(a[11])]
					i=0
					for s in systems :
						row[s] = sys[int(a[7+i])]
						i+=1
					writer.writerow(row)
			return bottle.static_file('db.csv', root=os.path.dirname(os.path.abspath(__file__)),download='db.csv')
		else :
			return "Error: the requested type of export ("+post_get('type')+") is unknown. Please choose \"DB\" or \"CSV\"."
	else:
		book = model.get_book_variable_module_name('config')
		data={'APP_PREFIX':request.app.config['myapp.APP_PREFIX'], 'config': book, 'error': 'Bad Token !'}
		return bottle.template('export',data)

# Access to local static files
@app.route('/static/:type/:filename#.*#')
def send_static(type, filename):
	return bottle.static_file(filename, root=os.path.join(os.path.dirname(os.path.abspath(__file__)),'static/%s/') % type)

# Access to local static media files
@app.route('/media/:filename#.*#')
def send_static(filename):
	return bottle.static_file(filename, root=os.path.join(os.path.dirname(os.path.abspath(__file__)),'media/'))

# # Access to local static sound files
# @app.route('/media/:media/:syst/:filename#.*#')
# @app.route('/media/:media/./:syst/:filename#.*#')
# def send_static(media, syst, filename):
# 	return bottle.static_file(filename, root=os.path.join(os.path.dirname(os.path.abspath(__file__)),'media/%s/') % media+'/'+syst)

@app.route('/:badroute')
def badroute(badroute):
	bottle.redirect(request.app.config['myapp.APP_PREFIX']+'/test')

def main():
	bottle.run(app_middlware, host='localhost', port=8080, server='paste', reloader=True)
if __name__ == '__main__':
	main()
else:
	application = app_middlware
