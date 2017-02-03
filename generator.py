# -*- coding: utf-8 -*-
import argparse
import csv
import json
import os
import random
import re
import shutil
import sqlite3
import string
import sys
from pprint import pprint
from pm_bodies import platform_body, model_body

execfile(os.path.join(os.path.dirname(__file__), 'pm_bodies.py'))

# global variables
csv_delimiter = ';'
nbSystemToDisplay = 1
prefix = ''
tok = ''
useMedia = []
verbose = False
warning = []


def parse_arguments():
	print('	╔════════════════╗')
	print('	║  GENERATOR.PY  ║')
	print('	╚════════════════╝')
	print('')

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
		addWarning('bad csv delimiter. The default delimiter (;) is used.')
	if verbose:
		print('csv_delimiter is: ' + csv_delimiter)

	lsPath = []
	lsName = []
	if args.name:
		for index, elt in enumerate(args.systems):
			if index % 2 == 0:
				lsPath.append(elt)
			else:
				lsName.append(elt)
		if len(lsName) != len(lsPath):
			exit_on_error('bad number of arguments (in systems argument)')
	else:
		lsPath = args.systems

	return args.json, lsPath, lsName, args.main_tpl, args.index_tpl, args.completed_tpl, args.export_tpl


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


def create_architecture(testName):
	if verbose:
		print('|-----------------------|')
		print('| architecture creation |')
		print('v-----------------------v')

	def create_dir(path, name):
		std_dir = str(path) + str(name)
		dir = std_dir
		i = 0
		while os.path.exists(dir):
			if verbose:
				print('Folder ' + dir + ' already exist.')
			i += 1
			dir = std_dir + '_' + str(i)
		if i > 0:
			addWarning('Folder ' + std_dir + ' already exist.')
			addWarning('New folder at ' + dir)
		os.makedirs(dir)
		if verbose:
			print(dir + ' created.')
		return dir + '/'

	simpleTestName = re.sub('\W', '_', testName)

	mainDirectory = os.path.join(os.path.dirname(__file__), 'tests/')
	if not os.path.exists(mainDirectory):
		os.makedirs(mainDirectory)

	testDirectory = create_dir(mainDirectory, simpleTestName)
	viewsDirectory = create_dir(testDirectory, 'views')
	staticDirectory = create_dir(testDirectory, 'static')
	mediaDirectory = create_dir(testDirectory, 'media')

	if verbose:
		print('Done.\n')
	return mainDirectory, testDirectory, viewsDirectory, staticDirectory, mediaDirectory


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
		exit_on_error('Invalid JSON file: no configuration object founded')
	if verbose:
		print('Configuration JSON:')
		print(configJson)

	# json expected and mandatory input definition
	expectedStringConfig = {
	'author' : '\'unknown\'',
	'name' : '\'TEST\'',
	'nbFixedPosition' : '\'0\'',
	'nbIntroductionSteps' : '\'0\''
	}
	expectedListConfig = {
	'useMedia':'[]'
	}
	mandatoryStringConfig = ['nbSampleBySystem', 'nbSteps', 'nbSystemDisplayed', 'nbQuestions', 'prefix']
	mandatoryListConfig = ['headersCSV']

	def writeString(var1):
		if type(configJson[var1]) == unicode:
			config.write((var1 + '=\'' + configJson[var1] + '\'\n').encode('UTF-8'))
		else:
			config.write(var1 + '=\'' + str(configJson[var1]) + '\'\n')
	def writeList(var2):
		config.write(var2 + '=[')
		for i,elt in enumerate(configJson[var2]):
			config.write('\''+elt.encode('UTF-8')+'\'')
			if i < len(configJson[var2])-1:
				config.write(',')
		config.write(']\n')

	# config file writing
	config = open(testDirectory + '/config.py', 'w')
	config.write('# -*- coding: utf-8 -*-\n')
	config.write('# === CONFIGURATION VARIABLES ===\n')
	config.write('# Each configuration variable is necessarily a string or a list of string\n')
	with open(lsPath[0], 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
		nbsbs = sum(1 for row in spamreader)
	checkHeadersCSV = []
	for var in configJson:
		if var in mandatoryStringConfig:
			writeString(var)
			mandatoryStringConfig.remove(var)
		elif var in mandatoryListConfig:
			writeList(var)
			mandatoryListConfig.remove(var)
		elif var in expectedStringConfig:
			writeString(var)
			del expectedStringConfig[var]
		elif var in expectedListConfig:
			writeList(var)
			del expectedListConfig[var]
		else:
			writeString(var)

		# special cases
		if var == 'nbSystemDisplayed':
			nbSystemToDisplay = int(configJson[var])
		elif var == 'prefix':
			prefix = configJson[var]
		elif var == 'useMedia':
			useMedia = [x.encode('UTF-8') for x in configJson[var]]
		elif var == 'headersCSV':
			checkHeadersCSV = [x.encode('UTF-8') for x in configJson[var]]
		elif var == 'nbFixedPosition':
			if configJson[var] < 0 or configJson[var] > configJson['nbSteps']:
				configJson[var] = nbsbs

	# expected and mandatory checks
	for mandatory in mandatoryStringConfig:
		exit_on_error('Invalid JSON file: '+mandatory+' is mandatory')
	for mandatory in mandatoryListConfig:
		exit_on_error('Invalid JSON file: '+mandatory+' is mandatory')

	for expected in expectedStringConfig:
		config.write((expected + '=\'' + expectedStringConfig[expected] + '\'\n').encode('UTF-8'))
	for expected in expectedListConfig:
		config.write((expected + '=\'' + expectedListConfig[expected] + '\'\n').encode('UTF-8'))

	# write extra config
	tok = generate_token()
	config.write('token=\'' + tok + '\'\n')
	config.write('nbSampleBySystem=\'' + str(nbsbs) + '\'\n')

	# check if each useMedia is in headersCSV
	if 'useMedia' in globals():
		for aUseMedia in useMedia:
			errorInUseMedia = True
			for aHCSV in checkHeadersCSV:
				if aHCSV == aUseMedia:
					errorInUseMedia = False
			if errorInUseMedia:
				exit_on_error('value "'+aUseMedia+'" in useMedia is not in headersCSV (in JSON config file)')
	if verbose:
		print('Done.\n')


def load_csv(listOfPath, config):
	if verbose:
		print('|-------------|')
		print('| loading CSV |')
		print('v-------------v')

	headersCSV = config['configuration']['headersCSV']
	lsCSV = []
	for csvPath in listOfPath:
		if not os.path.isfile(csvPath):
			exit_on_error(csvPath + ' must be a file')
		with open(csvPath, 'rb') as csvfile:
			if csv_delimiter == 'tab':
				spamreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
			else:
				spamreader = csv.reader(csvfile, delimiter=csv_delimiter, quotechar='"')

			data = []
			for i, row in enumerate(spamreader):
				if verbose:
					print(', '.join(row))
				if len(row)!=len(headersCSV):
					exit_on_error(csvPath +' is not valid: columns number is not correct at line '+str(i+1))
				data.append(row)
			lsCSV.append(data)
	if verbose:
		print('list of CSV:')
		print(lsCSV)
	return lsCSV


def create_db(config, data, listOfName):
	if verbose:
		print('|---------------|')
		print('| DB generation |')
		print('v---------------v')

	con = sqlite3.connect(testDirectory + '/data.db')
	headersCSV = config['configuration']['headersCSV']
	if not listOfName:
		if verbose:
			print('No system names defined. Default system names will be created:')
		for index, system in enumerate(data):
			listOfName.append('system_' + str(index))
			if verbose:
				print('system_' + str(index))
	try:
		systs = '`system1` TEXT NOT NULL'
		for i in range(1, nbSystemToDisplay):
			systs = systs + ', `system' + str(i + 1) + '` TEXT NOT NULL'
		columns = ''
		for header in headersCSV:
			columns += '`'+header+'` TEXT NOT NULL,'
		con.execute('CREATE TABLE system (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `name` TEXT NOT NULL)')
		con.execute('CREATE TABLE sample (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, '+columns+' `type` TEXT NOT NULL, `id_system` TEXT NOT NULL , `sample_index` INTEGER NOT NULL, `nb_processed` INTEGER NOT NULL DEFAULT 0, FOREIGN KEY(id_system) REFERENCES system(id))')
		con.execute('CREATE TABLE answer (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `user` TEXT NOT NULL, `date` TEXT NOT NULL, `content` TEXT NOT NULL, `content_target` TEXT, `sample_index` INTEGER NOT NULL, `question_index` INTEGER NOT NULL,'+systs+' )')
		con.commit()
		if verbose:
			print('Database successfully created.')
		try:
			for index, system in enumerate(data):
				con.execute('INSERT INTO system(name) VALUES (?)', (listOfName[index],))
				for i, sample in enumerate(system):
					if i < config['configuration']['nbIntroductionSteps']:
						sampleType = 'intro'
					else:
						sampleType = 'test'
					sampleTuple = ()
					for j in sample:
						sampleTuple += (j,)
					sampleTuple += (sampleType, index + 1, i,)
					con.execute('INSERT INTO sample('+', '.join(headersCSV)+', type, id_system, sample_index) VALUES ('+'?,'*len(headersCSV)+'?,?,?)', sampleTuple)
			con.commit()
			if verbose:
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


def copy_templates(inputTemplatePath, indexTemplatePath, completedTemplatePath, exportTemplatePath):
	if verbose:
		print('|----------------|')
		print('| templates copy |')
		print('v----------------v')

	shutil.copy(inputTemplatePath, viewsDirectory + 'template.tpl')
	shutil.copy(indexTemplatePath, viewsDirectory + 'index.tpl')
	shutil.copy(completedTemplatePath, viewsDirectory + 'completed.tpl')
	shutil.copy(exportTemplatePath, viewsDirectory + 'export.tpl')

	if verbose:
		print('Done.\n')


def create_platform():
	if verbose:
		print('|-------------------|')
		print('| platform creation |')
		print('v-------------------v')

	fo = open(testDirectory + 'platform.py', 'wb')
	fo.write(platform_body)
	fo.close()
	if verbose:
		print('Done.\n')


def create_model():
	if verbose:
		print('|----------------|')
		print('| model creation |')
		print('v----------------v')

	fo = open(testDirectory + 'model.py', 'wb')
	fo.write(model_body)
	fo.close()
	if verbose:
		print('Done.\n')


def copy_media(csv):
	if verbose:
		print('|-----------------|')
		print('| media file copy |')
		print('v-----------------v')

	media = []
	audioFolders = []
	regex = '^.*\/'
	for system in csv:
		for sample in system:
			for col_index, col_content in enumerate(sample):
				if configJSON['configuration']['headersCSV'][col_index].encode('UTF-8') in useMedia:
					media.append(col_content)
	for wav in media:
		search = re.search(regex, wav)
		if search:
			if search.group(0) not in audioFolders:
				audioFolders.append(search.group(0))
	for folder in audioFolders:
		os.makedirs(mediaDirectory + folder)
	for file in media:
		filedir = ''
		search = re.search(regex, file)
		if search:
			filedir = search.group(0)
		try:
			shutil.copy(file, mediaDirectory + filedir)
		except Exception:
			exit_on_error(file + ' is not a correct path')
		if verbose:
			print(file + '  to  ' + mediaDirectory + filedir)
	if verbose:
		print('Done.\n')


def addWarning(warningMessage):
	warning.append(warningMessage)


def printWarning():
	print('')
	for i in warning:
		print('WARNING: ' + i)


def generate_token():
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(30))


def exit_on_error(fatal_message):
	shutil.rmtree(testDirectory)
	sys.exit('ABORT: '+fatal_message)


(inputJSON, lsPath, lsName, inputTemplate, indexTemplate, completedTemplate, exportTemplate) = parse_arguments()
configJSON = load_json(inputJSON)
(mainDirectory, testDirectory, viewsDirectory, staticDirectory, mediaDirectory) = create_architecture(configJSON['configuration']['name'])
generate_config(configJSON, lsPath)
listDataCSV = load_csv(lsPath, configJSON)
create_db(configJSON, listDataCSV, lsName)
copy_templates(inputTemplate, indexTemplate, completedTemplate, exportTemplate)
create_platform()
create_model()
if 'useMedia' in globals():
	copy_media(listDataCSV)
url = ''
if prefix != '':
	url = 'server_url/' + prefix + '/export'
else:
	url = 'server_url/export'

print('    GENERATION TERMINEE !!')
print('=' * 30)
printWarning()
print('')
print('You can access the database at the following url: ' + url)
print('Token = ' + tok)
print('')
