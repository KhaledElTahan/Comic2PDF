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
	extensions = [".cbr", ".rar", ".cbz", ".zip"]

	try:
		for ext in extensions:
			if os.path.exists(file + ext):
				os.remove(file + ext)

	except Exception as e: 
		print(e)


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
	print("+S Removing RAR/ZIP/CBR/CBZ files")
	for directory in directories:
		files = os.listdir(directory)
		for file in files:
			if file[-4:] == '.pdf':
				removeFile(directory + "\\" + file[:-4])
	print ("+E Removing RAR/ZIP/CBR/CBZ files is done")

	print("Cleanup is Done")
	

if __name__ == "__main__":
	recursive()