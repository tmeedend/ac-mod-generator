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
	updateModUrlForAcServer = False
	carDownloadUrlPrefix=""
	trackDownloadUrlPrefix=""
	overrideArchives=False
	forceOverride=False

	def readMandatoryConfigField(self, configJsonFile, field):
		value = configJsonFile[field]
		if value == None or value == '':
			sys.exit("Cannot read field " + field + " from actools config file")
		return value

	def argValueOrNone(self, args, argName):
		if argName in args and not args[argName] == None:
			return args[argName]
		return None

	def argPathOrNone(self, args, argName):
		value = self.argValueOrNone(args, argName)
		if not value == None:
			return value.replace("/", os.sep)
		return None

	def argValueOrFalse(self, args, argName):
		if argName in args and args[argName]:
			return True
		return False

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
		#if not os.path.isdir(self.acpath):
		#	sys.exit("Cannot find Assetto Corsa install folder. Exiting") 

		argsparser = argparse.ArgumentParser(description='Build/clean Assetto Corsa mods from mods archives or folders')
		argsparser.add_argument('-g','--update_mod_url', action='store_true', help='Generate the meta_data.json needed for acServer or update ui_car.json', required=False)
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

		self.updateModUrlForAcServer = self.argValueOrFalse(args, 'update_mod_url')
		self.forceOverride = self.argValueOrFalse(args, 'force_override')
		self.overrideArchives = self.argValueOrFalse(args, 'override_archives')
		self.trackDownloadUrlPrefix = self.argValueOrNone(args, 'track_url_prefix')
		self.carDownloadUrlPrefix = self.argValueOrNone(args, 'car_url_prefix')
		self.tracksDestination = self.argPathOrNone(args, 'tracks_destination')
		self.carsDestination = self.argPathOrNone(args, 'cars_destination')
		self.tracksToProcess = self.argValueOrNone(args, 'tracks')
		self.carsToProcess = self.argValueOrNone(args, 'cars')
		self.archiveToProcess = self.argValueOrNone(args, 'archive')

		

		if self.tracksDestination == None or self.tracksDestination == "":
			self.tracksDestination = os.getcwd()
			
		if self.carsDestination == None or self.carsDestination == "":
			self.carsDestination = os.getcwd()