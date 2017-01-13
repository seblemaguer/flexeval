import json
import csv
import os
import re
import shutil
import sqlite3
import sys
import argparse

from pprint import pprint

execfile(os.path.join(os.path.dirname(__file__),'pm_bodies.py'))
# nbSystemToDisplay = 2
# useMedia = True
# verbose = False

def parse_arguments():
	JSONFile = None
	TemplateFile = None
	# parser = OptionParser()
	parser = argparse.ArgumentParser(description='Generator for subjective test web platform')
	parser.add_argument('-j', '--json', help='input JSON file', type=argparse.FileType('r'), required=True)
	parser.add_argument('-t', '--tpl', help='input template file', type=str, required=True)
	parser.add_argument('-i', '--index-tpl', help='input index template file', type=str, required=True)
	parser.add_argument('-c', '--completed-tpl', help='input last page template file', type=str, required=True)
	parser.add_argument('-s', '--systems', nargs='+', help='list of systems', type=str, required=True)
	parser.add_argument('-n', '--name', help='systems with names after', action='store_true')
	parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true')
	args = parser.parse_args()

	global verbose 
	verbose = args.verbose

	lsPath = []
	lsName = []
	if(args.name):
		for index, elt in enumerate(args.systems):
			if index%2==0:
				lsPath.append(elt)
			else:
				lsName.append(elt)
		if len(lsName) != len(lsPath):
			sys.exit('ABORT: Bad number of arguments (in systems argument)')
	else:
		lsPath = args.systems

	return args.json, lsPath, lsName, args.tpl, args.index_tpl, args.completed_tpl

def create_architecture(testName):
	print('|-----------------------|')
	print('| architecture creation |')
	print('v-----------------------v')

	def create_dir(path, name):
		dir = str(path)+str(name)+'/'
		if os.path.exists(dir):
			sys.exit('ABORT: Folder already exist : '+dir)
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

	data = json.load(JSONfile)
	if verbose:
		pprint(data)

	print('Done.\n')
	return data

def load_csv(lsPath, lsName):
	print('|----------|')
	print('| load CSV |')
	print('v----------v')

	for csvPath in lsPath:
		if not os.path.isfile(csvPath):
			sys.exit('ABORT: '+csvPath+' must be a file')
		with open(csvPath, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
			if verbose:
				for row in spamreader:
					print ', '.join(row)

	# TODO: return csv_data + csv_headers

def create_db(data):
	print('|---------------|')
	print('| DB generation |')
	print('v---------------v')

	con = sqlite3.connect(testDirectory+'/data.db')
	try:
		systs = '`system1` TEXT NOT NULL'
		for i in range(1,nbSystemToDisplay):
			systs = systs + ', `system'+str(i+1) + '` TEXT NOT NULL'
		con.execute('CREATE TABLE system (`id` TEXT NOT NULL PRIMARY KEY UNIQUE, `name` TEXT NOT NULL, `comment` TEXT NOT NULL)')
		con.execute('CREATE TABLE sample (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `path` TEXT NOT NULL, `type` TEXT NOT NULL, `id_system` TEXT NOT NULL , `syst_index` INTEGER NOT NULL, `nb_processed` INTEGER NOT NULL DEFAULT 0, FOREIGN KEY(id_system) REFERENCES system(id))')
		con.execute('CREATE TABLE answer (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `user` TEXT NOT NULL, `date` TEXT NOT NULL, `content` TEXT NOT NULL, `content_target` TEXT, `syst_index` INTEGER NOT NULL, `question_index` INTEGER NOT NULL,'+systs+' )')
		con.commit()
		print('Database successfully created.')
		for system in data['systems']['system']:
			systemIndex = 0
			systemToInsert = (system['id'],system['name'],system['comment'])
			con.execute('INSERT INTO system(id, name, comment) VALUES (?,?,?)', systemToInsert)
			for samples in system['samples']:
				sampleType = samples['type']
				for samplePath in samples['sample']:
					sampleToInsert=(samplePath, sampleType, system['id'], systemIndex)
					con.execute('INSERT INTO sample(path, type, id_system, syst_index) VALUES (?,?,?,?)', sampleToInsert)
					systemIndex += 1
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
	global useMedia
	configJson = json
	if 'configuration' in configJson:
		configJson = configJson['configuration']
	else:
		sys.exit('ABORT: Invalid JSON file')

	print('Configuration JSON:')
	print(configJson)

	expectedConfig = ['name', 'author', 'nbSteps', 'nbIntroductionSteps', 'nbSystemDisplayed', 'description', 'welcomeText', 'useMedia', 'nbQuestions', 'nbFixedPosition']

	config = open(testDirectory+'/config.py', 'w')
	config.write('# === CONFIGURATION VARIABLES ===\n')
	config.write('# Each configuration variable is necessarily a string\n')
	samples = json['systems']['system'][0]['samples']
	nbsbs = 0
	for s in samples :
		if s['type']=='test' :
			nbsbs = len(s['sample'])
	for var in configJson:
		if var in expectedConfig:
			print(var+'\t:: OK')
			expectedConfig.remove(var)
		if var=='nbSystemDisplayed':
			nbSystemToDisplay = int(configJson[var])
		elif var == 'useMedia':
			useMedia = configJson[var]=="True"
		elif var == 'nbFixedPosition' :
			if configJson[var] < 0 or configJson[var] > configJson['nbSteps'] :
				configJson[var]=nbsbs
		config.write(var+'=\''+str(configJson[var])+'\'\n')
	for expected in expectedConfig:
		print(expected+' not found!')
		if expected == 'name':
			config.write(expected+'=\'TEST\'\n')
		if expected == 'author':
			config.write(expected+'=\'unknow\'\n')
		if expected == 'nbQuestions':
			print('ERROR :: '+expected)
			sys.exit('ABORT: Invalid JSON file')
		if expected == 'nbSteps':
			print('ERROR :: '+expected)
			sys.exit('ABORT: Invalid JSON file')
		if expected == 'nbIntroductionSteps':
			config.write(expected+'=\'0\'\n')
		if expected == 'nbSystemDisplayed':
			print('ERROR :: '+expected)
			sys.exit('ABORT: Invalid JSON file')
		if expected == 'description':
			config.write(expected+'=\'\'\n')
		if expected == 'welcomeText':
			config.write(expected+'=\'\'\n')
		if expected == 'useMedia':
			config.write(expected+'=\'True\'\n')
		if expected == 'nbFixedPosition' :
			config.write(expected+'=\'0\'\n')
	config.write('nbSampleBySystem=\''+str(nbsbs)+'\'\n')
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
	print('Done.\n')

def create_platform():
	print('|--------------------|')
	print('| platform creation |')
	print('v--------------------v')
	fo = open(testDirectory+'platform.py', 'wb')
	fo.write(platform_body)
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
			print("ERRROR \t:: "+ et + " not found! Please add it our you will get trouble...")
			miss=miss+1
	if miss==0 :
		print("Static Files \t:: OK")
	miss=0
	for t in warning_tags:
		for i in range(nbSystemToDisplay) :
			matches = re.findall("{{"+t+"\[["+str(i)+"]+\]}}", filetext)
			checked.append("{{"+t+"["+str(i)+"]}}")
			if len(matches)==0:
				print(t + " \t:: ERROR - missing "+t+"["+str(i)+"] tag in your template!")
	if miss==0 :
		print("Dynamics tags \t:: OK")
	matches = re.findall(regexp, filetext)
	for m in matches :
		if m in checked :
			continue
		if not m in authorized_tags :
			print(m + " \t:: WARN : maybe you have an error in your template, please check if your application works fine !")
		else :
			print(m + " \t:: OK")
		checked.append(m)
	print('Done.\n')

def copy_templates(inputTemplate, indexTemplate, completedTemplate):
	print('|----------------------|')
	print('|  copy templates      |')
	print('v----------------------v')
	shutil.copy(indexTemplate, viewsDirectory+'index.tpl')
	shutil.copy(inputTemplate, viewsDirectory+'template.tpl')
	shutil.copy(completedTemplate, viewsDirectory+'completed.tpl')
	
	print('Done.\n')


(inputJSON, lsPath, lsName, inputTemplate, indexTemplate, completedTemplate) = parse_arguments()
dataFromJSON = parse_json(inputJSON)
name = dataFromJSON['configuration']['name']
(mainDirectory, testDirectory, viewsDirectory, staticDirectory, mediaDirectory) = create_architecture(name)
generate_config(dataFromJSON)
load_csv(lsPath, lsName)
create_db(dataFromJSON)
# generate_template() # TODO: not used, move to verif_template
copy_templates(inputTemplate, indexTemplate, completedTemplate)
create_platform()
create_model()
if useMedia:
	copy_media(dataFromJSON)
# verif_template() # TODO: rewrite this function

print('='*30)
print('    GENERATION TERMINEE !!')
print('='*30)
