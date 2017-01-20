# -*- coding: utf-8 -*-
import argparse
import csv
import json
import os
import re
import shutil
import sqlite3
import sys
from pprint import pprint
import random
import string

execfile(os.path.join(os.path.dirname(__file__),'pm_bodies.py'))
global prefix
prefix=''
global tok
tok=''
global warning
warning=[]

def parse_arguments():
	print('	╔════════════════╗')
	print('	║  GENERATOR.PY  ║')
	print('	╚════════════════╝')
	print('')

	JSONFile = None
	TemplateFile = None
	parser = argparse.ArgumentParser(description='Generator for subjective test web platform')
	parser.add_argument('-j', '--json', help='input JSON file', type=argparse.FileType('r'), required=True)
	parser.add_argument('-t', '--main-tpl', help='input main template file', type=str, required=True)
	parser.add_argument('-i', '--index-tpl', help='input index template file', type=str, required=True)
	parser.add_argument('-c', '--completed-tpl', help='input last page template file', type=str, required=True)
	parser.add_argument('-e', '--export-tpl', help='export page template file', type=str, required=True)
	parser.add_argument('-s', '--systems', nargs='+', help='list of systems', type=str, required=True)
	parser.add_argument('-n', '--name', help='allow names after each systems (default: no names)', action='store_true')
	parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true')
	parser.add_argument('--csv-delimiter', help='define csv delimiter (default: ;)', default=';')
	args = parser.parse_args()

	global verbose 
	verbose = args.verbose
	if verbose:
		print('verbose mode enabled')
	global csv_delimiter
	if len(args.csv_delimiter) == 1 or args.csv_delimiter == 'tab':
		csv_delimiter = args.csv_delimiter
	elif len(args.csv_delimiter) == 3 and args.csv_delimiter[0] == '\'' and args.csv_delimiter[2] == '\'':
		csv_delimiter = args.csv_delimiter[1]
	else:
		print('Warning: bad csv delimiter. The default delimiter is used.')
	if verbose:
		print('csv_delimiter is: '+csv_delimiter)
	
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

	return args.json, lsPath, lsName, args.main_tpl, args.index_tpl, args.completed_tpl, args.export_tpl

def create_architecture(testName):
	if verbose:
		print('|-----------------------|')
		print('| architecture creation |')
		print('v-----------------------v')

	def create_dir(path, name):
		std_dir = str(path)+str(name)
		dir = std_dir
		i = 0
		while os.path.exists(dir):
			if verbose:
				print('Folder '+dir+' already exist.')
			i+=1
			dir = std_dir+'_'+str(i)
		if i>0:
			addWarning('Folder '+std_dir+' aready exist.')
			addWarning('New folder at '+dir)
		os.makedirs(dir)
		if verbose:
			print(dir+' created.')
		return dir+'/'

	simpleTestName = re.sub('\W','_', testName)

	mainDirectory = os.path.join(os.path.dirname(__file__),'tests/')
	if not os.path.exists(mainDirectory):
		os.makedirs(mainDirectory)

	testDirectory = create_dir(mainDirectory, simpleTestName)
	viewsDirectory = create_dir(testDirectory, 'views')
	staticDirectory = create_dir(testDirectory, 'static')
	mediaDirectory = create_dir(testDirectory, 'media')

	if verbose:
		print('Done.\n')
	return mainDirectory, testDirectory, viewsDirectory, staticDirectory, mediaDirectory

def load_json(JSONfile):
	if verbose:
		print('|--------------|')
		print('| loading JSON |')
		print('v--------------v')

	data = json.load(JSONfile)
	if verbose:
		pprint(data)

	if verbose:
		print('Done.\n')
	return data

def load_csv(lsPath):
	if verbose:
		print('|-------------|')
		print('| loading CSV |')
		print('v-------------v')

	lsCSV = []
	for csvPath in lsPath:
		if not os.path.isfile(csvPath):
			sys.exit('ABORT: '+csvPath+' must be a file')
		with open(csvPath, 'rb') as csvfile:
			if csv_delimiter == 'tab':
				spamreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
			else:
				spamreader = csv.reader(csvfile, delimiter=csv_delimiter, quotechar='"')

			data = []
			for row in spamreader:
				if verbose:
					print(', '.join(row))
				data.append(row)
			lsCSV.append(data)
	if verbose:
		print('list of CSV:')
		print(lsCSV)
	return lsCSV

def create_db(config, data, lsName):
	if verbose:
		print('|---------------|')
		print('| DB generation |')
		print('v---------------v')

	con = sqlite3.connect(testDirectory+'/data.db')
	headersCSV = config['configuration']['headersCSV']
	if not lsName:
		if verbose:
			print('No system names defined. Default system names will be created:')
		for index, system in enumerate(data):
			lsName.append('system_'+str(index))
			if verbose:
				print('system_'+str(index))
	try:
		systs = '`system1` TEXT NOT NULL'
		for i in range(1,nbSystemToDisplay):
			systs = systs + ', `system'+str(i+1) + '` TEXT NOT NULL'
		columns = ''
		for header in headersCSV:
			columns += '`'+header+'` TEXT NOT NULL,'
		con.execute('CREATE TABLE system (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `name` TEXT NOT NULL)')
		con.execute('CREATE TABLE sample (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, '+columns+' `type` TEXT NOT NULL, `id_system` TEXT NOT NULL , `syst_index` INTEGER NOT NULL, `nb_processed` INTEGER NOT NULL DEFAULT 0, FOREIGN KEY(id_system) REFERENCES system(id))')
		con.execute('CREATE TABLE answer (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `user` TEXT NOT NULL, `date` TEXT NOT NULL, `content` TEXT NOT NULL, `content_target` TEXT, `syst_index` INTEGER NOT NULL, `question_index` INTEGER NOT NULL,'+systs+' )')
		con.commit()
		if verbose:
			print('Database successfully created.')
		try:
			for index, system in enumerate(data):
				con.execute('INSERT INTO system(name) VALUES (?)', (lsName[index],))
				for i, sample in enumerate(system):
					if i < config['configuration']['nbIntroductionSteps']:
						sampleType = 'intro'
					else:
						sampleType = 'test'
					sampleTuple = ()
					for j in sample:
						sampleTuple += (j,)
					sampleTuple += (sampleType, index+1, i,)
					con.execute('INSERT INTO sample('+', '.join(headersCSV)+', type, id_system, syst_index) VALUES ('+'?,'*len(headersCSV)+'?,?,?)', sampleTuple)
			con.commit()
			if verbose :
				print('Database successfully filled.')
		except Exception as e:
			print('Exception in filling')
			con.rollback()
			raise e
	except Exception as e:
		print('Exception in creation')
		con.rollback()
		raise e
	finally:
		con.close()
	if verbose:
		print('Done.\n')

def generate_config(json, lsPath):
	if verbose:
		print('|-------------------|')
		print('| config generation |')
		print('v-------------------v')
	global nbSystemToDisplay
	global useMedia
	global prefix
	global tok
	configJson = json
	if 'configuration' in configJson:
		configJson = configJson['configuration']
	else:
		sys.exit('ABORT: Invalid JSON file')
	if verbose :
		print('Configuration JSON:')
		print(configJson)

	expectedConfig = ['name', 'author', 'nbSteps', 'nbIntroductionSteps', 'nbSystemDisplayed', 'description', 'useMedia', 'nbQuestions', 'nbFixedPosition']

	config = open(testDirectory+'/config.py', 'w')
	config.write('# === CONFIGURATION VARIABLES ===\n')
	config.write('# Each configuration variable is necessarily a string\n')
	nbsbs = 0
	with open(lsPath[0], 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
		nbsbs = sum(1 for row in spamreader)
	exception=[]
	for var in configJson:
		if var in expectedConfig:
			if verbose :
				print(var+'\t:: OK')
			expectedConfig.remove(var)
		if var=='nbSystemDisplayed':
			nbSystemToDisplay = int(configJson[var])
		elif var=="prefixe":
			prefix = configJson[var]
		elif var == 'useMedia':
			useMedia = configJson[var]
			config.write(var+'='+str(configJson[var])+'\n')
			exception.append(var)
		elif var == 'headersCSV' :
			config.write(var+'='+str(configJson[var])+'\n')
			exception.append(var)
		elif var == 'nbFixedPosition' :
			if configJson[var] < 0 or configJson[var] > configJson['nbSteps'] :
				configJson[var]=nbsbs
		if var not in exception:
			if type(configJson[var]) == unicode:
				config.write((var+'=\''+configJson[var]+'\'\n').encode('UTF-8'))
			else:
				config.write(var+'=\''+str(configJson[var])+'\'\n')
	tok = generate_token()
	config.write('token=\''+tok+'\'\n')
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
		if expected == 'useMedia':
			config.write(expected+'=[]\n')
		if expected == 'nbFixedPosition' :
			config.write(expected+'=\'0\'\n')
	config.write('nbSampleBySystem=\''+str(nbsbs)+'\'\n')
	if verbose:
		print('Done.\n')

def generate_template():
	if verbose:
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
	if verbose:
		print('Done.\n')

def create_platform():
	if verbose:
		print('|-------------------|')
		print('| platform creation |')
		print('v-------------------v')
	fo = open(testDirectory+'platform.py', 'wb')
	fo.write(platform_body)
	fo.close()
	if verbose:
		print('Done.\n')

def create_model():
	if verbose:
		print('|----------------|')
		print('| model creation |')
		print('v----------------v')
	fo = open(testDirectory+'model.py', 'wb')
	fo.write(model_body)
	fo.close()
	if verbose:
		print('Done.\n')

def copy_media(csv, mediaColumns, config):
	if verbose:
		print('|-----------------|')
		print('| media file copy |')
		print('v-----------------v')

	audio = []
	audioFolders = []
	systems = []
	regex = '^.*\/'
	systems = csv
	for system in csv:
		for sample in system:
			for col_index,col_content in enumerate(sample):
				if configJSON['configuration']['headersCSV'][col_index] in mediaColumns:
					audio.append(col_content)
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
		if verbose:
			print(file+'  to  '+mediaDirectory+filedir)
	if verbose:
		print('Done.\n')

def verif_template():
	if verbose:
		print('|----------------|')
		print('| template check |')
		print('v----------------v')
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
			print('ERRROR \t:: '+ et + ' not found! Please add it our you will get trouble...')
			miss=miss+1
	if miss==0 :
		print('Static Files \t:: OK')
	miss=0
	for t in warning_tags:
		for i in range(nbSystemToDisplay) :
			matches = re.findall("{{"+t+"\[["+str(i)+"]+\]}}", filetext)
			checked.append("{{"+t+"["+str(i)+"]}}")
			if len(matches)==0:
				print(t + ' \t:: ERROR - missing '+t+'['+str(i)+'] tag in your template!')
	if miss==0 :
		print('Dynamics tags \t:: OK')
	matches = re.findall(regexp, filetext)
	for m in matches :
		if m in checked :
			continue
		if not m in authorized_tags :
			print(m + ' \t:: WARN : maybe you have an error in your template, please check if your application works fine !')
		else :
			print(m + ' \t:: OK')
		checked.append(m)
	if verbose:
		print('Done.\n')

def copy_templates(inputTemplate, indexTemplate, completedTemplate, exportTemplate):
	if verbose:
		print('|----------------|')
		print('| templates copy |')
		print('v----------------v')
	shutil.copy(indexTemplate, viewsDirectory+'index.tpl')
	shutil.copy(inputTemplate, viewsDirectory+'template.tpl')
	shutil.copy(completedTemplate, viewsDirectory+'completed.tpl')
	shutil.copy(exportTemplate, viewsDirectory+'export.tpl')
	
	if verbose:
		print('Done.\n')

def addWarning(warningMessage):
	warning.append(warningMessage)

def printWarning():
	for i in warning:
		print('WARNING: '+i)


def generate_token():
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(30))


(inputJSON, lsPath, lsName, inputTemplate, indexTemplate, completedTemplate, exportTemplate) = parse_arguments()
configJSON = load_json(inputJSON)
(mainDirectory, testDirectory, viewsDirectory, staticDirectory, mediaDirectory) = create_architecture(configJSON['configuration']['name'])
generate_config(configJSON, lsPath)
listDataCSV = load_csv(lsPath)
create_db(configJSON, listDataCSV, lsName)
copy_templates(inputTemplate, indexTemplate, completedTemplate, exportTemplate)
create_platform()
create_model()
if useMedia:
	copy_media(listDataCSV, useMedia, configJSON)
url=''
if prefix!='' : 
	url='server_url/'+prefix+'/export'
else :
	url='server_url/export'


print('You can access the database from the following url : ' + url)
print('You will need a token for this, so keep this one !!')
print('Token = '+tok)
printWarning()
print('='*30)
print('    GENERATION TERMINEE !!')
print('='*30)
