import os
import subprocess
import sys
import tempfile
import json
import argparse

from actools import common

class Params:

	sevenzipexec = None
	acpath = None

	tracksToProcess = None
	carsToProcess = None
	archiveToProcess = None
	modsDestDir = None
	createAcServerMetatadaFile = False
	downloadUrlPrefix=None
	overrideExistingArchives=False


	def readMandatoryConfigField(self, configJsonFile, field):
		value = configJsonFile[field]
		if value == None or value == '':
			sys.exit("Cannot read field " + field + " from actools config file")
		return value


	def checkEnv(self):
		try:
			configJsonFile = common.parseJson('actools-config.json')
		except Exception as e:
			print(e)
			sys.exit("Cannot read actools config file. Exiting") 
		self.sevenzipexec = self.readMandatoryConfigField(configJsonFile, '7zipexec').replace("/", os.sep)
		self.acpath = self.readMandatoryConfigField(configJsonFile, 'assetto-corsa-install-folder').replace("/", os.sep)
		
		if not os.path.isfile(self.sevenzipexec):
			sys.exit("Cannot find 7zip executable. Exiting") 
		if not os.path.isdir(self.acpath):
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

		if 'gen-metadata-file' in args:
			self.createAcServerMetatadaFile = True
		if 'override-existing-archive' in args:
			self.overrideExistingArchives = True
		if 'url-prefix' in args:
			self.downloadUrlPrefix = args['url-prefix']
		if 'destination' in args:
			self.modsDestDir = args['destination']
		if 'tracks' in args:
			self.tracksToProcess = args['tracks']
		if 'cars' in args:
			self.carsToProcess = args['cars']
		if 'archive' in args:
			self.archiveToProcess = args['archive']
		

		if self.modsDestDir == None or self.modsDestDir == "":
			self.modsDestDir = os.getcwd()