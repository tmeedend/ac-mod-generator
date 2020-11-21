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
	tracksDestination = None
	carsDestination = None
	createAcServerMetatadaFile = False
	carDownloadUrlPrefix=""
	trackDownloadUrlPrefix=""
	overrideArchives=False
	forceOverride=False

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
		argsparser.add_argument('-g','--gen_metadata_file', action='store_true', help='Generate the meta_data.json needed for acServer', required=False)
		argsparser.add_argument('-f','--force_override', action='store_true', help='If an archive already exists in the destination folder, it will be overriden, no matter the dates', required=False)
		argsparser.add_argument('-o','--override_archives', action='store_true', help='If an archive already exists in the destination folder, it will be overriden if the mod has a newer file than the archive to override', required=False)
		argsparser.add_argument('-tu','--track_url_prefix', help='The URL prefix to write into the acServer meta_data.json file for tracks, for the url field', required=False)
		argsparser.add_argument('-cu','--car_url_prefix', help='The URL prefix to write into the acServer meta_data.json file for cars, for the url field', required=False)
		argsparser.add_argument('-td','--tracks_destination', help='If specified, the generated archives will be generated here instead of the current dir', required=False)
		argsparser.add_argument('-cd','--cars_destination', help='If specified, the generated archives will be generated here instead of the current dir', required=False)
		argsparser.add_argument('-t','--tracks', help='The name of the tracks to archive from the assetto corsa install dir. If the value is #all, it will archive all the tracks.', required=False)
		argsparser.add_argument('-c','--cars', help='The name of the tracks to archive from the assetto corsa install dir. If the value is #all, it will archive all the cars.', required=False)
		argsparser.add_argument('-a','--archive', help='The path to a mod archive to transform to a good mod structure that can be enabled/disabled by Content Manager', required=False)
		args = vars(argsparser.parse_args())

		if 'gen_metadata_file' in args and args['gen_metadata_file']:
			self.createAcServerMetatadaFile = True
		if 'force_override' in args and args['force_override']:
			self.forceOverride = True
		if 'override_archives' in args and args['override_archives']:
			self.overrideArchives = True
		if 'track_url_prefix' in args:
			self.trackDownloadUrlPrefix = args['track_url_prefix']
		if 'car_url_prefix' in args:
			self.carDownloadUrlPrefix = args['car_url_prefix']
		if 'tracks_destination' in args:
			self.tracksDestination = args['tracks_destination']
		if 'cars_destination' in args:
			self.carsDestination = args['cars_destination']
		if 'tracks' in args:
			self.tracksToProcess = args['tracks']
		if 'cars' in args:
			self.carsToProcess = args['cars']
		if 'archive' in args:
			self.archiveToProcess = args['archive']
		

		if self.tracksDestination == None or self.tracksDestination == "":
			self.tracksDestination = os.getcwd()
			
		if self.carsDestination == None or self.carsDestination == "":
			self.carsDestination = os.getcwd()