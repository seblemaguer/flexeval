import json
import os
import re
import shutil
import sqlite3
import sys
from pprint import pprint
from optparse import OptionParser

execfile(os.path.join(os.path.dirname(__file__),'pm_bodies.py'))
nbSystemToDisplay=2

def parser_options_jt():
	parser = OptionParser()
	parser.add_option('-j', '--json', dest='inputJSON', help='input JSON file', metavar='FILE')
	parser.add_option('-t', '--tpl', dest='inputTemplate', help='input template file', metavar='FILE')
	inputJSON = None
	inputTemplate = None
	(options, args) = parser.parse_args()
	if(options.inputJSON==None) :
		sys.exit('Invalid JSON file name')
	else :
		inputJSON = options.inputJSON
	if(options.inputTemplate==None) :
		sys.exit('Invalid template file name')
	else :
		inputTemplate = options.inputTemplate
	return inputJSON, inputTemplate

def create_architecture(testName):
	print('|-----------------------|')
	print('| architecture creation |')
	print('v-----------------------v')

	def create_dir(path, name):
		dir = str(path)+str(name)+'/'
		if os.path.exists(dir):
			sys.exit('Folder already exist : '+dir)
		os.makedirs(dir)
		print(dir+' created.')
		return dir

	mainDirectory = os.path.join(os.path.dirname(__file__),'tests/')
	if not os.path.exists(mainDirectory):
		os.makedirs(mainDirectory)

	testDirectory = create_dir(mainDirectory, testName)
	viewsDirectory = create_dir(testDirectory, 'views')
	staticDirectory = create_dir(testDirectory, 'static')
	mediaDirectory = create_dir(testDirectory, 'media')

	print('Done.\n')
	return mainDirectory, testDirectory, viewsDirectory, staticDirectory, mediaDirectory

def parse_json(JSONfile):
	print('|--------------|')
	print('| parsing JSON |')
	print('v--------------v')

	with open(JSONfile) as data_file:
		data = json.load(data_file)
	pprint(data)

	print('Done.\n')
	return data

def create_db(data):
	print('|---------------|')
	print('| DB generation |')
	print('v---------------v')

	con = sqlite3.connect(testDirectory+'/data.db')
	try:
		systs="`system1` TEXT NOT NULL"
		for i in range(1,int(nbSystemToDisplay)):
			systs=systs + ", `system"+str(i+1)+"` TEXT NOT NULL"
		con.execute("CREATE TABLE system (`id` TEXT NOT NULL PRIMARY KEY UNIQUE, `name` TEXT NOT NULL, `comment` TEXT NOT NULL)")
		con.execute("CREATE TABLE sample (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `path` TEXT NOT NULL, `type` TEXT NOT NULL, `id_system` TEXT NOT NULL , `syst_index` INTEGER NOT NULL, `nb_processed` INTEGER NOT NULL DEFAULT 0, FOREIGN KEY(id_system) REFERENCES system(id))")
		con.execute("CREATE TABLE answer (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `user` TEXT NOT NULL, `date` TEXT NOT NULL, `content` TEXT NOT NULL, `content_target` TEXT, `syst_index` INTEGER NOT NULL, `question_index` INTEGER NOT NULL,"+systs+" )")
		con.commit()
		print('Database successfully created.')
		for system in data['systems']['system']:
			systemIndex = 0
			systemToInsert=(system['-id'],system['-name'],system['comment'])
			con.execute("INSERT INTO system(id, name, comment) VALUES (?,?,?)", systemToInsert)
			for samples in system['samples']:
				sampleType=samples['-type']
				for samplePath in samples['sample']:
					systemIndex = systemIndex + 1
					sampleToInsert=(samplePath, sampleType, system['-id'], systemIndex)
					con.execute("INSERT INTO sample(path, type, id_system, syst_index) VALUES (?,?,?,?)", sampleToInsert)
		con.commit()
		print('Database successfully filled.')
	except Exception as e:
		print('EXCEPTION')
		con.rollback()
		raise e
	finally:
		con.close()
	print('Done.\n')

def generate_config(json):
	print('|-------------------|')
	print('| config generation |')
	print('v-------------------v')
	global nbSystemToDisplay
	configJson = json
	if 'configuration' in configJson:
		configJson = configJson['configuration']
	elif 'config' in configJson:
		configJson = configJson['config']
	elif 'conf' in configJson:
		configJson = configJson['conf']
	print('Configuration JSON:')
	print(configJson)

	config = open(testDirectory+'/'+'config.py', 'w')
	config.write('# === CONFIGURATION VARIABLES ===\n')
	config.write('# Each configuration variable is necessarily a string\n')
	for var in configJson:
		config.write(var+'=\''+configJson[var]+'\'\n')
		if var=="nbSystemDisplayed" :
			nbSystemToDisplay = int(configJson[var])
	questions = json['questions']
	print('Questions JSON:')
	print(questions)
	config.write('nbQuestions=\"'+str(len(questions['question']))+'\"\n')
	samples = json['systems']['system'][0]['samples']
	nbsbs = 0
	for s in samples :
		if s['-type']=='test' :
			nbsbs = len(s['sample'])
	config.write('nbSampleBySystem=\''+str(nbsbs)+'\'\n')
	questions = json['questions']['question']
	qtype=[]
	for i in range(len(questions)):
		qtype.append('"'+questions[i]['type']+'"')
	config.write('questionsType=['+','.join(qtype)+']\n')
	print('Done.\n')

def generate_template():
	print('|---------------------|')
	print('| template generation |')
	print('v---------------------v')

	shutil.copy(inputTemplate, viewsDirectory)
	print('template correctly moved to '+viewsDirectory)

	print('TEMPLATE VERIFICATION:')

	tplPath = ''
	regexName = '[^\/]+$'
	regexLink = '<(l|L)(i|I)(n|N)(k|K).+href=.+>'
	regexScript = '<(s|S)(c|C)(r|R)(i|I)(p|P)(t|T).+src=.+>'
	linkArray = []
	scriptArray = []

	search = re.search(regexName, inputTemplate)
	if search :
		tplPath = viewsDirectory+search.group(0)
	print('template at "'+tplPath+'":')

	tpl = open(tplPath, 'r').read()
	for finditer in re.finditer(regexLink, tpl):
		linkArray.append(finditer.group(0))
	for finditer in re.finditer(regexScript, tpl):
		scriptArray.append(finditer.group(0))
	print(linkArray)
	print(scriptArray)
	# search = re.search(regex, tpl)
	# if search :
	# 	print(search)
	print('Done.\n')

def create_plateform():
	print('|--------------------|')
	print('| plateform creation |')
	print('v--------------------v')
	fo = open(testDirectory+'plateform.py', 'wb')
	fo.write(plateform_body)
	fo.close()
	print('Done.\n')

def create_model():
	print('|----------------|')
	print('| model creation |')
	print('v----------------v')
	fo = open(testDirectory+'model.py', 'wb')
	fo.write(model_body)
	fo.close()
	print('Done.\n')

def copy_media(json):
	print('|-----------------|')
	print('| media file copy |')
	print('v-----------------v')

	audio = []
	audioFolders = []
	systems = []
	regex = '^.*\/'
	systems = json['systems']['system']
	for samples in systems:
		for sample in samples['samples']:
			for wav in sample['sample']:
				audio.append(wav)
	for wav in audio:
		search = re.search(regex, wav)
		if search :
			if search.group(0) not in audioFolders:
				audioFolders.append(search.group(0))
	for folder in audioFolders:
		os.makedirs(mediaDirectory+folder)
	for file in audio:
		filedir = ''
		search = re.search(regex, file)
		if search :
			filedir = search.group(0)
		shutil.copy(file, mediaDirectory+filedir)
		print(file+'  to  '+mediaDirectory+filedir)
	print('Done.\n')

def verif_template():
	print('|-----------------|')
	print('| template check  |')
	print('v-----------------v')
	authorized_tags=["{{name}}","{{author}}","{{description}}","{{index}}","{{user}}"]
	warning_tags=["samples","systems"]
	essentials_tags=["bootstrap.min.css","jquery.js","jquery-ui.min.js","jquery-ui.min.css","addEventListener"]
	regexp = '{{[A-z,0-9]+}}'
	textfile = open(inputTemplate, 'r')
	filetext = textfile.read()
	textfile.close()
	checked=[]
	miss=0
	for et in essentials_tags :
		matches = re.findall(et, filetext)
		if len(matches)==0:
			print "ERRROR \t :: "+ et + " not found! Please add it our you will get trouble..."
			miss=miss+1
	if miss==0 :
		print "Static Files \t :: OK!"
	miss=0
	for t in warning_tags:
		for i in range(nbSystemToDisplay) :
			matches = re.findall("{{"+t+"\[["+str(i)+"]+\]}}", filetext)
			checked.append("{{"+t+"["+str(i)+"]}}")
			if len(matches)==0:
				print m + " \t:: ERROR - missing "+t+"["+str(i)+"] tag in your template!"
	if miss==0 :
		print "Dynamics tags \t :: OK!"
	matches = re.findall(regexp, filetext)
	for m in matches :
		if m in checked :
			continue
		if not m in authorized_tags :
			print m + " \t:: WARN : maybe you have an error in your template, please check if your application works fine !"
		else :
			print m + " \t:: OK"
		checked.append(m)
	print('Done.\n')

def add_login():
	print('|----------------------|')
	print('|  add login template  |')
	print('v----------------------v')
	fo = open(viewsDirectory+'login_form.tpl', 'wb')
	fo.write(login_form)
	fo.close()
	print('Done.\n')

def add_extra_pages():
	print('|-----------------------|')
	print('|  add extra templates  |')
	print('v-----------------------v')
	fo = open(viewsDirectory+'index.tpl', 'wb')
	fo.write(index_form)
	fo.close()
	print('Done.\n')



(inputJSON, inputTemplate) = parser_options_jt()
dataFromJSON = parse_json(inputJSON)
name = dataFromJSON['configuration']['name']
(mainDirectory, testDirectory, viewsDirectory, staticDirectory, mediaDirectory) = create_architecture(name)
generate_config(dataFromJSON)
create_db(dataFromJSON)
generate_template()
create_plateform()
create_model()
add_login()
add_extra_pages()
copy_media(dataFromJSON)
verif_template()

print('='*30)
print('    GENERATION TERMINEE !!')
print('='*30)

# platform.py		OK
# model.py			OK
# config.py			OK
# db.db				OK
# audio/*.wav		OK
# template.tpl		a verifier