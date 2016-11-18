import json
import os
import sqlite3
import sys
from pprint import pprint



def parseJSON(JSONfile):
	print("|--------------|")
	print("| parsing JSON |")
	print("v--------------v")

	with open(JSONfile) as data_file:
		data = json.load(data_file)
	pprint(data)

	return data

def createDB(data, directory):
	print("|-------------|")
	print("| DB creation |")
	print("v-------------v")

	con = sqlite3.connect(directory+"/data.db")
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

def fillMainDB(data):
	print("|-----------------|")
	print("| main DB filling |")
	print("v-----------------v")

	maxIndex = -1

	con = sqlite3.connect("./databases/static_db.db") # Warning: This file is created in the current directory
	try:
		cursor = con.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS test (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `name` TEXT NOT NULL, `author` TEXT, `nbInstances` TEXT, `nbSteps` TEXT, `nbConsistencySteps` TEXT, `nbIntroductionSteps` TEXT, `description` TEXT, `start` TEXT, `end` TEXT)")

		conf = data["test"]["configuration"]
		confToInsert = (conf["name"], conf["author"], conf["nbInstances"], conf["nbSteps"], conf["nbConsistencySteps"], conf["nbIntroductionSteps"], conf["description"], conf["start"], conf["end"])
		cursor.execute("INSERT INTO test(name, author, nbInstances, nbSteps, nbConsistencySteps, nbIntroductionSteps, description, start, end) VALUES (?,?,?,?,?,?,?,?,?)", confToInsert)

		con.commit()

		print("Successfully filled database.")

		cursor.execute("SELECT max(id) FROM test")
		maxIndex = cursor.fetchone()[0]
		print "Max index =", maxIndex
	except Exception as e:
		print("EXCEPTION")
		con.rollback()
		raise e
	finally:
		con.close()
		return maxIndex

def generateTemplate(type):
	print("|---------------------|")
	print("| template generation |")
	print("v---------------------v")

	tpl = open("template.tpl", "w")

def generateConfig(data):
	print("|-------------------|")
	print("| config generation |")
	print("v-------------------v")

	tpl = open(testDirectory+"/"+"config.py", "w")



mainDirectory = "./tests"
if not os.path.exists(mainDirectory):
	os.makedirs(mainDirectory)

name = "newTest"
if len(sys.argv) == 2:
	name = sys.argv[1]
if os.path.exists(mainDirectory+"/"+name):
	sys.exit("ERREUR : dossier deja existant !")

testDirectory = mainDirectory+"/"+name
os.makedirs(testDirectory)

dataFromJSON = parseJSON("./test.json")

generateConfig(dataFromJSON)

createDB(dataFromJSON, testDirectory)




# lastIndex = fillMainDB(dataFromJSON)
# createDB("test-"+str(lastIndex), dataFromJSON)
# generateTemplate("toto")





# platform.py		à copier
# model.py			à copier
# config.py			à remplir
# db.db				OK
# audio/*.wav		à copier
# template.tpl		à copier et vérifier