
import json
import shutil
import subprocess
import os
import glob 
from configparser import ConfigParser

def cleanName(name, replaceSpacesByUnderscores):
	remove_punctuation_map = dict((ord(char), None) for char in '\/*?:"<>|')
	withoutPonctuation = name.translate(remove_punctuation_map)
	if replaceSpacesByUnderscores:
		return withoutPonctuation.replace(" ", "_")
	return withoutPonctuation

def parseJson(jsonfilename):
	try:
		return json.loads(open(jsonfilename, encoding='utf-8-sig').read(), strict=False)
	except:
		return json.loads(open(jsonfilename).read(), strict=False)

def fileContainsWord(filePath, word):
	try:
		with open(filePath) as f:
			if word in f.read():
				return True
	except:
		with open(filePath, encoding='utf-8-sig') as f:
			if word in f.read():
				return True
	return False

def getNewestFile(modPath):
	list_of_files = [result for result in glob.glob(modPath + '/**', recursive=True)  if not os.path.isdir(result) 
	and not result.endswith("meta_data.json") and not result.endswith("ui_car.json")  and not result.endswith("ui_track.json") and not result.endswith("payloads.bin") ]
	latest_file = max(list_of_files, key=os.path.getmtime)
	#print('\tlatest file is ' + latest_file + " date: %s" % time.ctime(os.path.getmtime(latest_file)))
	return os.path.getmtime(latest_file)

def unzipFileToDir(sevenzipexec, archiveFile, destination):
	if archiveFile.lower().endswith(".tgz") or archiveFile.lower().endswith(".tar.gz"):
		archiveCmd = "tar -zxf " + archiveFile + " --directory " + destination
	else:
		archiveCmd = sevenzipexec + ' x "' + archiveFile + '" -o"' + destination + '"'
	runCommand(archiveCmd)

def readIniFile(iniFile):
	# some mods use /// (Race Sim Studio) to add comments, clean them as it would break the .ini parsing
	# for line in fileinput.input(iniFile, inplace=True):
	#	line = re.sub('(.)*//(/)+','', line.rstrip())
	#	print(line)
	try:
		config = ConfigParser(strict=False, allow_no_value=True)
		config.read(iniFile)
		return config
	except:
		config = ConfigParser(strict=False, allow_no_value=True)
		config.read(iniFile, encoding='utf_8_sig')
		return config

def extractAcd(quickbmsexec, dataAcdFile, destination):
	archiveCmd = quickbmsexec + ' "' + 'acd.bms' + '"  "' + dataAcdFile + '" "' + destination + '"'
	runCommand(archiveCmd, True)


def runCommand(archiveCmd, quiet = True):
	# print('\texecuting ' + archiveCmd)
	# proc = subprocess.Popen(archiveCmd)
	if quiet:
		proc = subprocess.Popen(archiveCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	else:
		proc = subprocess.Popen(archiveCmd)
	#while proc.poll() is None:
	#	time.sleep(0.5)
	#	print("p21")
	#	data = proc.stdout.readline()
	#	percents = re.findall('\\d*%', data.decode())
	#	if len(percents) > 0:
	#		print ("percent" + percents[0])
	proc.communicate()	

def zipFileToDir(sevenzipexec, workingDirectory, archiveFile, listfilename, override, excludeArgs):
	origWD = os.getcwd() # remember our original working directory
	try:
		os.chdir(workingDirectory) 
		if os.path.isfile(archiveFile):
			if override:
				print("\tRemoving old archive file " + archiveFile)
				os.remove(archiveFile)
			else:
				print("\tarchive file " + archiveFile + " already exists. Skipping")
				return
		if listfilename == None:
			archiveCmd = sevenzipexec + ' a "' + archiveFile + '" *'
		else: 
			archiveCmd = sevenzipexec + ' a "' + archiveFile + '" -spf @' + listfilename
		if not excludeArgs  == None:
			archiveCmd = archiveCmd + " -xr!" + excludeArgs
		runCommand(archiveCmd)
	except:
		print("\tError while archiving mod") 
	finally:
		os.chdir(origWD) # get back to our original working directory 


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)