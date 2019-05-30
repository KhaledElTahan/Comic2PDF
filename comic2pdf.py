# Converts .cbr and .cbz files to .pdf
#
# Use:  python comic2pdf.py
# -- Only works with comicbook files that contain JPG's (for now).
# -- The script should be in the same directory the file(s) to convert are in.
#
# Author:  MComas1
# Date:  14-09-18
#
# License:  You can do what you want with it.
# Mainly based on a script by Bransorem (https://github.com/bransorem/comic2pdf) 

import os, sys, zipfile, patoolib, stat
from PIL import Image
import PIL.ExifTags
import uuid
import time

failed = False

def nlog_info (msg, out=open("comic2pdf_log.txt","a")):
    """Print info message to stdout (or any other given output)."""
    print("patool:", msg, file=out)


def olog_info (msg, out=sys.stdout):
    """Print info message to stdout (or any other given output)."""
    print("patool:", msg, file=out)


def trimFileNameSpace(file):
	new_file = file[:-4].rstrip() + file[-4:]
	os.rename(file, new_file)
	return new_file


def handlerar(filein, directory):
	tmp_dir = directory + "\\" + "TEMP2PDF" + str(uuid.uuid4()) + "\\"
	os.mkdir(tmp_dir)
	original = sys.stdout
	sys.stdout = open("comic2pdf_log.txt","a")
	patoolib.util.log_info = nlog_info
	patoolib.extract_archive(filein, outdir=tmp_dir)
	newfile = filein.replace(filein[-4:],".pdf")
	toPDF(newfile,tmp_dir)
	cleanDir(tmp_dir)
	print("------------------------------------------------------------")
	sys.stdout = original
	print("\""+newfile+"\" successfully converted!")


def handlezip(filein, directory):
	zip_ref = zipfile.ZipFile(filein, 'r')
	tmp_dir = directory + "\\" + "TEMP2PDF" + str(uuid.uuid4()) + "\\"
	zip_ref.extractall(tmp_dir)
	zip_ref.close()
	newfile = filein.replace(filein[-4:],".pdf")
	toPDF(newfile, tmp_dir)
	cleanDir(tmp_dir)
	print("\""+newfile+"\" successfully converted!")
	

def toPDF(filename, newdir):
	ffiles = getAllImagesPaths(newdir)

	# imagelist is the list with all image filenames
	im_list = list()
	firstP = True
	im = None
	for image in ffiles:
		im1 = Image.open(image)
		im1.load()
		
		if (firstP):
			im = im1
			firstP = False
		else: im_list.append(im1)

	im.save(filename, "PDF", resolution=100.0, save_all=True, append_images=im_list)
	
	cleanDir(newdir)


extensions = [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG", ".gif", ".GIF"]

def isImagePath(path):
	for ext in extensions:
		if path.endswith(ext):
			return True
	
	return False


def getAllImagesPaths(dir):
	result = []

	directories = [x[0] for x in os.walk(dir)]
	for directory in directories:
		ffiles = os.listdir(directory)

		for file in ffiles:
			if isImagePath(file):
				result.append(directory+"\\"+file)

	return result


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


def opendir(directory):
	for file in os.listdir(directory):
		try:
			if (file[-4:] == '.cbz' or file[-4:] == '.zip'):
				handlezip(trimFileNameSpace(directory+"\\"+file), directory)
			elif (file[-4:] == '.cbr' or file[-4:] == '.rar'):
				handlerar(trimFileNameSpace(directory+"\\"+file), directory)
		except Exception as e:
			print(e)
			print("FAILED:: " + directory + "\\" + file)



def recursive():
	directories = [x[0] for x in os.walk(os.getcwd())]

	for directory in directories:
		print("START:: Working in Directory: " + directory)
		opendir(directory)
		print("END:: Working in Directory: " + directory + "\n")

	print ("Conversion Done")


if __name__ == "__main__":	
	recursive()