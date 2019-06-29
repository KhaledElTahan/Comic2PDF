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


def _dummyOutput(s):
	pass


def file2PDF(filein, directory, type):
	tmp_dir = directory + "\\" + "TEMP2PDF" + str(uuid.uuid4()) + "\\"

	try:
		if type == "RAR":
			os.mkdir(tmp_dir)
			patoolib.util.log_info = _dummyOutput
			patoolib.extract_archive(filein, outdir=tmp_dir)
		elif type == "ZIP":
			zip_ref = zipfile.ZipFile(filein, 'r')
			zip_ref.extractall(tmp_dir)
			zip_ref.close()

		newfile = filein.replace(filein[-4:], ".pdf")
		images2PDF(newfile, tmp_dir)
		cleanDir(tmp_dir)

		pdf_size = os.path.getsize(newfile)
		comic_size = os.path.getsize(filein)
		
		if pdf_size > comic_size * 3 or pdf_size * 3 < comic_size:
			os.remove(newfile)
			print("Produced file size is unacceptable :: Original {0:.3f} MB => PDF {1:.3f} MB".format(comic_size/(1024.0 * 1024.0), pdf_size/(1024.0 * 1024.0)))
			print("FAILED:: " + filein)
		else:
			print("\"" + newfile + "\" successfully converted!")
		
	except Exception as e:
		cleanDir(tmp_dir)
		print(e)
		print("FAILED:: " + filein)


def images2PDF(filename, newdir):
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
				result.append(directory + "\\" + file)

	return result


def cleanDir(dir):
	directories = [x[0] for x in os.walk(dir)][1:]
	for directory in directories:
		cleanDir(directory)

	try:
		files = []

		if os.path.exists(dir):
			files = os.listdir(dir)

		for file in files:
			if os.path.exists(dir + "\\" + file):
				os.remove(dir + "\\" + file)

		if os.path.exists(dir):
			os.rmdir(dir)
	except Exception as e: 
		print(e)
		print("Failed to Clean Dir:: " + dir)


def trimFileNameSpace(file):
	new_file = file[:-4].rstrip() + file[-4:]
	os.rename(file, new_file)
	return new_file


def opendir(directory):
	for file in os.listdir(directory):
		if (file[-4:] == '.cbz' or file[-4:] == '.zip'):
			file2PDF(trimFileNameSpace(directory + "\\" + file), directory, "ZIP")
		elif (file[-4:] == '.cbr' or file[-4:] == '.rar'):
			file2PDF(trimFileNameSpace(directory + "\\" + file), directory, "RAR")


def recursive():
	directories = [x[0] for x in os.walk(os.getcwd())]

	for directory in directories:
		print("START:: Working in Directory: " + directory)
		opendir(directory)
		print("END:: Working in Directory: " + directory + "\n")

	print ("Conversion Done")


if __name__ == "__main__":	
	recursive()