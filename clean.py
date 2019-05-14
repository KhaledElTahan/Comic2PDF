import os

def cleanDir(dir):
	directories = [x[0] for x in os.walk(dir)][1:]
	for directory in directories:
		cleanDir(directory)

	try:
		files = os.listdir(dir)
		for file in files:
			os.remove(dir+"\\"+file)

		os.rmdir(dir)
	except Exception as e: 
		# print(e)
		# print(dir)
		pass

def removeFile(file):
	try:
		os.remove(file + ".cbr")
	except:
		pass

	try:
		os.remove(file + ".cbz")
	except:
		pass


def recursive():
	print ("Peforming Cleanup")

	directories = [x[0] for x in os.walk(os.getcwd())]

	print("+S Removing Temp Directory")
	for directory in directories:
		if "TEMP2PDF" in directory:
			print("++ Remove:: " + directory)
			cleanDir(directory)
	print ("+E Removing Temp Directories is done")


	directories = [x[0] for x in os.walk(os.getcwd())]
	print("+S Removing PDF files")
	for directory in directories:
		files = os.listdir(directory)
		for file in files:
			if file[-4:] == '.pdf':
				removeFile(directory + "\\" + file[:-4])
	print ("+E Removing PDF files is done")

	print("Cleanup is Done")


recursive()