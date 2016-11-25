
def fillMainDB(data):
	print("|-----------------|")
	print("| config  filling |")
	print("v-----------------v")

	with open('somefile.txt', 'w') as confile:
		conf = data["test"]["configuration"]

    	confile.write("class Config :\n")
    	confile.write("\tdef __init__(self):\n")
    	confile.write("self.id=\"Mytest\"")
    	confile.write("self.author=\""+conf["author"]+"\"")
    	confile.write("self.nbInstances=\""+conf["nbInstances"]+"\"")
    	confile.write("self.nbSteps=\""+conf["nbSteps"]+"\"")
    	confile.write("self.nbConsistencySteps=\""+conf["nbConsistencySteps"]+"\"")
    	confile.write("self.nbIntroductionSteps=\""+conf["nbIntroductionSteps"]+"\"")
    	confile.write("self.nbSteps=\""+conf["nbSteps"]+"\"")
    	confile.write("self.description=\""+conf["description"]+"\"")
    	confile.write("self.start=\""+conf["start"]+"\"")
    	confile.write("self.end=\""+conf["end"]+"\"")
    	
    	
