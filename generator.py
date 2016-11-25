import json
import os
import re
import shutil
import sqlite3
import sys
from pprint import pprint
from optparse import OptionParser

execfile("./p&m_bodies.py")

parser = OptionParser()
parser.add_option("-j", "--json", dest="inputJSON", help="input JSON file", metavar="FILE")
parser.add_option("-t", "--tpl", dest="inputTemplate", help="input template file", metavar="FILE")
inputJSON = ""
inputTemplate = ""
(options, args) = parser.parse_args()
if(options.inputJSON==None or options.inputJSON=="") :
	sys.exit("Invalid JSON file name")
else :
	inputJSON = options.inputJSON

if(options.inputTemplate==None or options.inputTemplate=="") :
	sys.exit("Invalid template file name")
else :
	inputTemplate = options.inputTemplate


def createArchitecture(testName):
	print("|-----------------------|")
	print("| architecture creation |")
	print("v-----------------------v")

	def createDir(path, name):
		dir = str(path)+str(name)+"/"
		if os.path.exists(dir):
			sys.exit("Folder already exist : "+dir)
		os.makedirs(dir)
		print(dir+" created.")
		return dir

	mainDirectory = "./tests/"
	if not os.path.exists(mainDirectory):
		os.makedirs(mainDirectory)

	testDirectory = createDir(mainDirectory, testName)
	viewsDirectory = createDir(testDirectory, "views")
	staticDirectory = createDir(testDirectory, "static")
	mediaDirectory = createDir(testDirectory, "media")

	print("Done.\n")
	return mainDirectory, testDirectory, viewsDirectory, staticDirectory, mediaDirectory

def parseJSON(JSONfile):
	print("|--------------|")
	print("| parsing JSON |")
	print("v--------------v")

	with open(JSONfile) as data_file:
		data = json.load(data_file)
	pprint(data)

	print("Done.\n")
	return data

def createDB(data):
	print("|---------------|")
	print("| DB generation |")
	print("v---------------v")

	con = sqlite3.connect(testDirectory+"/data.db")
	try:
		con.execute("CREATE TABLE system (`id` TEXT NOT NULL PRIMARY KEY UNIQUE, `name` TEXT NOT NULL, `comment` TEXT NOT NULL)")
		con.execute("CREATE TABLE sample (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `path` TEXT NOT NULL, `type` TEXT NOT NULL, `id_system` TEXT NOT NULL , `syst_index` INTEGER NOT NULL, `nb_processed` INTEGER NOT NULL DEFAULT 0, FOREIGN KEY(id_system) REFERENCES system(id))")
		con.execute("CREATE TABLE answer (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `user` TEXT NOT NULL, `date` TEXT NOT NULL, `content` TEXT NOT NULL, `syst_index` INTEGER NOT NULL, `question_index` INTEGER NOT NULL)")
		con.commit()
		for system in data["test"]["systems"]["system"]:
			systemIndex = 0
			systemToInsert=(system["-id"],system["-name"],system["comment"])
			con.execute("INSERT INTO system(id, name, comment) VALUES (?,?,?)", systemToInsert)
			for samples in system["samples"]:
				sampleType=samples["-type"]
				for samplePath in samples["sample"]:
					systemIndex = systemIndex + 1
					sampleToInsert=(samplePath, sampleType, system["-id"], systemIndex)
					con.execute("INSERT INTO sample(path, type, id_system, syst_index) VALUES (?,?,?,?)", sampleToInsert)
		con.commit()

		print("Successfully created and filled database.")
	except Exception as e:
		print("EXCEPTION")
		con.rollback()
		raise e
	finally:
		con.close()
	print("Done.\n")

def generateConfig(json):
	print("|-------------------|")
	print("| config generation |")
	print("v-------------------v")

	config = open(testDirectory+"/"+"config.py", "w")
	if 'test' in json:	# TODO : penser a simplifier ce bout de code...
		configJson = json["test"]
		if 'configuration' in configJson:
			configJson = configJson["configuration"]
		elif 'config' in configJson:
			configJson = configJson["config"]
		elif 'conf' in configJson:
			configJson = configJson["conf"]
	elif 'configuration' in json:
		configJson = json["configuration"]
	elif 'config' in json:
		configJson = json["config"]
	elif 'conf' in json:
		configJson = json["conf"]
	print(configJson)

	config.write("# === CONFIGURATION VARIABLES ===\n")
	config.write("# Each configuration variable is necessarily a string\n")
	for var in configJson:
		config.write(var+"=\""+configJson[var]+"\"\n")
	config.write("\n")
	print("Done.\n")

def generateTemplate():
	print("|---------------------|")
	print("| template generation |")
	print("v---------------------v")

	print(inputTemplate)
	print(testDirectory)
	shutil.copy(inputTemplate, viewsDirectory)

	# TODO Verifier le template

	print("Done.\n")

def create_controller():
	print("|---------------------|")
	print("| controller creation |")
	print("v---------------------v")
	fo = open(testDirectory+"plateform.py", "wb")
	fo.write(controller_body)
	fo.close()
	print("Done.\n")

def create_model():
	print("|----------------|")
	print("| model creation |")
	print("v----------------v")
	fo = open(testDirectory+"model.py", "wb")
	fo.write(controller_body)
	fo.close()
	print("Done.\n")

def copyMedia(json):
	print("|-----------------|")
	print("| media file copy |")
	print("v-----------------v")

	audio = []
	audioFolders = []
	systems = []
	regexp = "^.*\/"
	if 'test' in json:
		systems = json["test"]["systems"]["system"]
	else:
		systems = json["systems"]["system"]
	for samples in systems:
		for sample in samples["samples"]:
			for wav in sample["sample"]:
				audio.append(wav)
	for wav in audio:
		search = re.search(regexp, wav)
		if search :
			if search.group(0) not in audioFolders:
				audioFolders.append(search.group(0))
	for folder in audioFolders:
		os.makedirs(mediaDirectory+folder)
	for file in audio:
		filedir = ""
		search = re.search(regexp, file)
		if search :
			filedir = search.group(0)
		shutil.copy(file, mediaDirectory+filedir)
	print("Done.\n")



dataFromJSON = parseJSON(inputJSON)

name = dataFromJSON["test"]["configuration"]["name"]

(mainDirectory, testDirectory, viewsDirectory, staticDirectory, mediaDirectory) = createArchitecture(name)

generateConfig(dataFromJSON)

createDB(dataFromJSON)

generateTemplate()

create_controller()

create_model()

copyMedia(dataFromJSON)




# platform.py		OK
# model.py			OK
# config.py			OK
# db.db				OK
# audio/*.wav		OK
# template.tpl		a verifier