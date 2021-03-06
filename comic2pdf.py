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

import os, sys, zipfile, patoolib
from PIL import Image
import PIL.ExifTags
import uuid
import time
import gc
from colorama import init, Fore, Back, Style
import sys

write = sys.stdout.write
init()

totalComicsNumber = None
currentComicNumber = 0

def _dummyOutput(s):
	pass


def file2PDF(filein, directory, type):
	global currentComicNumber, totalComicsNumber
	currentComicNumber = currentComicNumber + 1


	print("* [{0}/{1}] ".format(currentComicNumber, totalComicsNumber) + filein, end=" ")

	tmp_dir = directory + "\\" + "TEMP2PDF" + str(uuid.uuid4()) + "\\"
	newfile = None 

	try:
		comic_size = os.path.getsize(filein)

		print("{0:.3f} MB - Extracting".format(comic_size/(1024.0 * 1024.0)), end=" ")

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
		
		if pdf_size > comic_size * 3 or pdf_size * 3 < comic_size:
			os.remove(newfile)
			print(Fore.RED + "FAILURE")
			print("Produced file size is unacceptable :: Original {0:.3f} MB => PDF {1:.3f} MB".format(comic_size/(1024.0 * 1024.0), pdf_size/(1024.0 * 1024.0)))
			print(Style.RESET_ALL, end="")
		else:
			print(Fore.GREEN + "SUCCESS" + Style.RESET_ALL)
		
	except Exception as e:
		cleanDir(tmp_dir)
		if newfile is not None and os.path.exists(newfile):
			os.remove(newfile)
			
		print(Fore.RED + "FAILURE")
		print(e)
		print(Style.RESET_ALL, end="")


def images2PDF(filename, newdir):
	ffiles = getAllImagesPaths(newdir)

	# imagelist is the list with all image filenames
	im_list = list()
	firstP = True
	im = None

	length = len(ffiles)
	cnt = 1

	print("- Processing 000.00%", end=" ")

	for image in ffiles:
		im1 = Image.open(image)
		im1.load()
		
		if (firstP):
			im = im1
			firstP = False
		else: im_list.append(im1)

		write("\b" * 8)
		print("{0:.2f}%".format(cnt * 100.0 / length).zfill(7), end=" ")

		cnt = cnt + 1

	print("- Saving", end=" ")

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
		pass


def trimFileNameSpace(file):
	new_file = file[:-4].rstrip() + file[-4:]
	os.rename(file, new_file)
	return new_file


def opendir(directory):
	for file in os.listdir(directory):
		if (file[-4:] == '.cbz' or file[-4:] == '.zip'):
			file2PDF(trimFileNameSpace(directory + "\\" + file), directory, "ZIP")
			gc.collect()
		elif (file[-4:] == '.cbr' or file[-4:] == '.rar'):
			file2PDF(trimFileNameSpace(directory + "\\" + file), directory, "RAR")
			gc.collect()

def countComics():
	directories = [x[0] for x in os.walk(os.getcwd())]

	cnt = 0

	for directory in directories:
		for file in os.listdir(directory):
			if (file[-4:] == '.cbz' or file[-4:] == '.zip' or file[-4:] == '.cbr' or file[-4:] == '.rar'):
				cnt = cnt + 1

	return cnt


def recursive():
	global totalComicsNumber
	totalComicsNumber = countComics()

	directories = [x[0] for x in os.walk(os.getcwd())]
	
	for directory in directories:
		print("START:: Working in Directory: " + directory)
		opendir(directory)
		print("END:: Working in Directory: " + directory + "\n")

	print ("Conversion Done")


if __name__ == "__main__":	
	recursive()