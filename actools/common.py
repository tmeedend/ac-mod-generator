
import json
import subprocess
import os
import glob 
import time
from configparser import ConfigParser

def cleanName(name):
	remove_punctuation_map = dict((ord(char), None) for char in '\/*?:"<>|')
	return name.translate(remove_punctuation_map)

def parseJson(jsonfilename):
	try:
		return json.loads(open(jsonfilename, strict=False).read(), strict=False)
	except:
		return json.loads(open(jsonfilename, encoding='utf-8-sig').read(), strict=False)

def getNewestFile(modPath):
	list_of_files = glob.glob(modPath + '/**', recursive=True) 
	latest_file = max(list_of_files, key=os.path.getmtime)
	print('latest file is ' + latest_file + " date: %s" % time.ctime(os.path.getctime(latest_file)))
	return os.path.getctime(latest_file)

def unzipFileToDir(sevenzipexec, archiveFile, destination):
	archiveCmd = sevenzipexec + ' x ' + archiveFile + ' -o"' + destination + '"'
	print('executing ' + archiveCmd)
	subprocess.Popen(archiveCmd).communicate()

def readIniFile(iniFile):
	try:
		config = ConfigParser(strict=False)
		config.read(iniFile)
		return config
	except:
		config = ConfigParser(strict=False)
		config.read(iniFile, encoding='utf_8_sig')
		return config

def zipFileToDir(sevenzipexec, workingDirectory, archiveFile, listfilename, override, excludeArgs):
	origWD = os.getcwd() # remember our original working directory
	try:
		os.chdir(workingDirectory) 
		if os.path.isfile(archiveFile):
			if override:
				print("Removing old archive file " + archiveFile)
				os.remove(archiveFile)
			else:
				print("archive file " + archiveFile + " already exists. Skipping")
				return
		if listfilename == None:
			archiveCmd = sevenzipexec + ' a "' + archiveFile + '" *'
		else: 
			archiveCmd = sevenzipexec + ' a "' + archiveFile + '" -spf @' + listfilename
		if not excludeArgs  == None:
			archiveCmd = archiveCmd + " -xr!" + excludeArgs
		print('executing ' + archiveCmd)
		subprocess.Popen(archiveCmd).communicate()
	except:
		print("Error while archiving mod") 
	finally:
		os.chdir(origWD) # get back to our original working directory 