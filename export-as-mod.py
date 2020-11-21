import os
import subprocess
import sys
import tempfile
import json
import argparse
from actools import common

from actools import tracks
from actools import cars

sevenzipexec = None
acpath = None

tracksToProcess = None
carsToProcess = None
archiveToProcess = None
modsDestDir = None
createAcServerMetatadaFile = False
downloadUrlPrefix=None
overrideExistingArchives=False

def readMandatoryConfigField(configJsonFile, field):
	value = configJsonFile[field]
	if value == None or value == '':
		sys.exit("Cannot read field " + field + " from actools config file")
	return value

def checkEnv():
	global acpath
	global sevenzipexec
	try:
		configJsonFile = common.parseJson('actools-config.json')
	except Exception as e:
		print(e)
		sys.exit("Cannot read actools config file. Exiting") 
	sevenzipexec = readMandatoryConfigField(configJsonFile, '7zipexec').replace("/", os.sep)
	acpath = readMandatoryConfigField(configJsonFile, 'assetto-corsa-install-folder').replace("/", os.sep)
	
	if not os.path.isfile(sevenzipexec):
		sys.exit("Cannot find 7zip executable. Exiting") 
	if not os.path.isdir(acpath):
		sys.exit("Cannot find Assetto Corsa install folder. Exiting") 

	argsparser = argparse.ArgumentParser(description='Build/clean Assetto Corsa mods from mods archives or folders')
	argsparser.add_argument('-g','--gen-metadata-file', help='Generate the meta_data.json needed for acServer', required=False)
	argsparser.add_argument('-o','--override-existing-archive', help='If an archive already exists in the destination folder, it will be overriden', required=False)
	argsparser.add_argument('-u','--url-prefix', help='The URL prefix to write into the acServer meta_data.json file, for the url field', required=False)
	argsparser.add_argument('-d','--destination', help='If specified, the generated archives will be generated here instead of the current dir', required=False)
	argsparser.add_argument('-t','--tracks', help='The name of the tracks to archive from the assetto corsa install dir. If the value is #all, it will archive all the tracks.', required=False)
	argsparser.add_argument('-c','--cars', help='The name of the tracks to archive from the assetto corsa install dir. If the value is #all, it will archive all the cars.', required=False)
	argsparser.add_argument('-a','--archive', help='The path to a mod archive to transform to a good mod structure that can be enabled/disabled by Content Manager', required=False)
	args = vars(argsparser.parse_args())

	global createAcServerMetatadaFile
	global overrideExistingArchives
	global downloadUrlPrefix
	global modsDestDir
	global tracksToProcess
	global carsToProcess
	global archiveToProcess

	if 'gen-metadata-file' in args:
		createAcServerMetatadaFile = True
	if 'override-existing-archive' in args:
		overrideExistingArchives = True
	if 'url-prefix' in args:
		downloadUrlPrefix = args['url-prefix']
	if 'destination' in args:
		modsDestDir = args['destination']
	if 'tracks' in args:
		tracksToProcess = args['tracks']
	if 'cars' in args:
		carsToProcess = args['cars']
	if 'archive' in args:
		archiveToProcess = args['archive']
	

	if modsDestDir == None or modsDestDir == "":
		modsDestDir = os.getcwd

def processTracks():
	global acpath
	global modsDestDir
	if tracksToProcess != None and tracksToProcess.strip() != "":
		trackModTool = tracks.TrackTools(acpath, sevenzipexec)
		if tracksToProcess == "#all":
			trackModTool.packAllMods(modsDestDir, createAcServerMetatadaFile, overrideExistingArchives, downloadUrlPrefix, acpath)
		else:
			for track in tracksToProcess.split(","):
				trackModTool.packMod(track, modsDestDir, createAcServerMetatadaFile, overrideExistingArchives, downloadUrlPrefix, acpath)

def processCars():
	global acpath
	global modsDestDir
	if carsToProcess != None and carsToProcess.strip() != "":
		carModTool = cars.CarTools(acpath, sevenzipexec)
		if tracksToProcess == "#all":
			carModTool.packAllMods(modsDestDir, createAcServerMetatadaFile, overrideExistingArchives, downloadUrlPrefix, acpath)
		else:
			for car in carsToProcess.split(","):
				carModTool.packMod(car, modsDestDir, createAcServerMetatadaFile, overrideExistingArchives, downloadUrlPrefix, acpath)

checkEnv()
processTracks()