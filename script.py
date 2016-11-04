import sqlite3
import json
from pprint import pprint

def createDB(JSONfile):
	print("createDB\n")
	print("--------------")
	print(" parsing JSON ")
	print("--------------")
	with open(JSONfile) as data_file:
		data = json.load(data_file)

	pprint(data)

	print("-------------")
	print(" DB creation ")
	print("-------------")

	# print(data["test"]["configuration"]["author"])
	# print(data["test"]["systems"]["system"][0]["-id"])

	dbName = "tests"
	con = sqlite3.connect(dbName+".db") # Warning: This file is created in the current directory
	# con.execute("attach DATABASE '"+dbName+".db' as tests")
	con.execute("CREATE TABLE system (`id` TEXT NOT NULL PRIMARY KEY UNIQUE, `name` TEXT NOT NULL, `comment` TEXT NOT NULL)")
	con.execute("CREATE TABLE sample (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `path` TEXT NOT NULL, `type` TEXT NOT NULL, `id_system` TEXT NOT NULL , `syst_index` INTEGER NOT NULL, `nb_processed` INTEGER NOT NULL DEFAULT 0)")
	con.execute("CREATE TABLE answer (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `user` TEXT NOT NULL, `date` TEXT NOT NULL, `content` TEXT NOT NULL, `syst_index` INTEGER NOT NULL, `question_index` INTEGER NOT NULL)")

	con.commit()

	print("------------")
	print(" DB filling ")
	print("------------")

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
	con.close()




createDB("test.json")

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