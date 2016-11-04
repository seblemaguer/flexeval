import sys
import bottle
import sqlite3
import model
import json
import os

bottle.debug(True)
app = bottle.app()

max_test=12

#bottle post methods
def postd():
	return bottle.request.forms


def post_get(name, default=''):
	return bottle.request.POST.get(name, default).strip()


#home page
@bottle.route('/')
@bottle.view('home')
def home():
	return {}


#creation de tests
@bottle.route('/create_test')
@bottle.view('create_test')
def create_test():
	return {}


@bottle.post('/validate_test')
def validate():
	#stimulus = post_get("stimulus_id")
	title = post_get("title") # with DataBase SQLite
	description = post_get("text_description") # with DataBase SQLite
	questions = post_get("questions")	#array of question
	quesion_num = questions.len
	#insert int static db here
	data = {"title" : title, "description" : description, "question_num" : question_num}
	model.insert_test('databases/static_db.db', data)
	#create a new database and init it
	code = model.get_new_code()
	model.create_test(str(code)+'.db')
	model.insert_questions(code,questions)

	save_path = "./sounds/"+str(code)+"/"
	if not os.path.exists(save_path) :
		os.makedirs(save_path)

	model.create_test(str(code)+'.db')
	
	#WARNING FOR THE OTHER ELEMENT, WAIT TO GET MORE INFORMATIONS
	#TODO : complete this function !
	#get the json content
	#jsonContent = post_get("data")
	#array = json.load(jsonContent)
	#for elem in array :
		
	#find a way to get the samples....
	#... process data (json file) here
	return "<p>Test "+ title +" has been succefully created!</p>"



#test view
@bottle.route('/test/:test_code')
def content(test_code,step=1):
	#access the database to get informations about the test
	data = model.get_test_step(int(test_code))
	template = "test_content"
	#data = {"step":step, "code":test_code, "url1":file1, "description":description, "url2":file2, "question":question, "author":author, "authormail" : authormail, "questions" : questions}
	return bottle.template(template, data)


#----------------------------------------------------------------------------------------------------


@bottle.post('/test/:test_code/:step')
def next_step(test_code,step):
	#process post data to the database
	if int(step) < max_test :
		#call the police
		return content(test_code,int(step)+1)
	else :
		return "<p>Test complete ! Thank you for your contribution ! </p>"

#subjective test page
#this page is only called for the first step
#@bottle.route('/test/:test_code')
#def test_page(test_code):
	"""Test page"""
	#plusieurs informations sont a recuperer ici
	#il faut :
	# - le code du test (l'id)
	# - l'url des resources medias (locales ou en ligne)
	# - le type de test a mettre en place
	# - a voir si d'autres choses sont necessaires
	#check if the database exists for this test, if not display an error message

	view = 'test_contentABX'
	args = {'step':2, 'code':test_code, 'url1':"/wav/bird.wav", 'url2':"/wav/dolphin.wav", 'rl3':"/wav/dolphin.wav", 'type':1, 'max':40, 'desc':"lorem ipsum"}
	return bottle.template(view,args)

@bottle.route('/admin_test/:test_code')
@bottle.view('test_stats')
def test_stats(test_code):
	#return the stats about the test and dislay them in the view
	return {'code': test_code, 'nb_complete':0}

#access to local static files
@bottle.route('/:type/:filename#.*#')
def send_static(type, filename):
	if type in ['css', 'js', 'img', 'fonts']:
		return bottle.static_file(filename, root="./static/%s/" % type)
	elif type in ['wav'] :
		return bottle.static_file(filename, root="./sound/")
	else:
		bottle.abort(404, "File not found")

@bottle.route('/')

def main():
	application = app
	bottle.run(app, host='localhost', port=8080)

if __name__ == "__main__":
	main()