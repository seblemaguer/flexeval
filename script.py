import json
import sqlite3
import sys
from pprint import pprint

def parseJSON(JSONfile):
	print("\n> parseJSON\n")

	print("|--------------|")
	print("| parsing JSON |")
	print("v--------------v")

	with open(JSONfile) as data_file:
		data = json.load(data_file)
	pprint(data)

	return data

def createDB(dbName,data):
	print("\n> createDB\n")

	print("|-------------|")
	print("| DB creation |")
	print("v-------------v")

	con = sqlite3.connect("./databases/"+dbName+".db") # Warning: This file is created in the current directory
	try:
		con.execute("CREATE TABLE system (`id` TEXT NOT NULL PRIMARY KEY UNIQUE, `name` TEXT NOT NULL, `comment` TEXT NOT NULL)")
		con.execute("CREATE TABLE sample (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `path` TEXT NOT NULL, `type` TEXT NOT NULL, `id_system` TEXT NOT NULL , `syst_index` INTEGER NOT NULL, `nb_processed` INTEGER NOT NULL DEFAULT 0, FOREIGN KEY(id_system) REFERENCES system(id))")
		con.execute("CREATE TABLE answer (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `user` TEXT NOT NULL, `date` TEXT NOT NULL, `content` TEXT NOT NULL, `syst_index` INTEGER NOT NULL, `question_index` INTEGER NOT NULL)")
		con.commit()
		print("Successfully created database.")
	except Exception as e:
		con.rollback()
		raise e

	print("|------------|")
	print("| DB filling |")
	print("v------------v")

	try:
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

		print("Successfully filled database.")
	except Exception as e:
		print("EXCEPTION")
		con.rollback()
		raise e
	finally:
		con.close()

def fillMainDB(data):
	print("\n> fillMainDB\n")

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


dataFromJSON = parseJSON("./test.json")
lastIndex = fillMainDB(dataFromJSON)
createDB(str(lastIndex), dataFromJSON)

# print json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])

# def getTableDump(db_file, table_to_dump):
# 	conn = sqlite3.connect(':memory:')
# 	cursor = conn.cursor()
# 	cursor.execute("attach database '" + db_file + "' as attached_db")
# 	cursor.execute("select sql from attached_db.sqlite_master where type='table' and name='" + table_to_dump + "'")
# 	sql_create_table = cursor.fetchone()[0]
# 	cursor.execute(sql_create_table);
# 	cursor.execute("insert into " + table_to_dump + " select * from attached_db." + table_to_dump)
# 	conn.commit()
# 	cursor.execute("detach database attached_db")
# 	return "\n".join(conn.iterdump())

# TABLE_TO_DUMP = 'table_to_dump'
# DB_FILE = 'db_file'

# print getTableDump(DB_FILE, TABLE_TO_DUMP)