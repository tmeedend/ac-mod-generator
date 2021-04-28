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
	acmodspath = None
	quickbmsexec = None
	tracksToProcess = None
	carsToProcess = None
	archiveToProcess = None
	tracksDestination = None
	carsDestination = None
	addCspTags = False
	updateModUrlForAcServer = False
	skipKunosMods = False
	dontArchive = False
	carDownloadUrlPrefix=""
	trackDownloadUrlPrefix=""
	findTracksByTags=""
	findCarsByTags=""
	overrideArchives=False
	forceOverride=False
	clean=False
	guessToProcess=None
	appDir = None

	def __init__(self, appDir):
		self.appDir = appDir


	def readMandatoryConfigField(self, configIniFile, field):
		value = configIniFile.get('SETTINGS', field)
		if value == None or value == '':
			sys.exit("Cannot read field " + field + " from actools config file")
		return value

	def readConfigField(self, configIniFile, field):
		value = configIniFile.get('SETTINGS', field)
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

	def properAbsPath(self, path):
		return os.path.abspath(path.replace("/", os.sep)).strip(os.sep)

	def checkEnv(self):
		try:
			configIniFile = common.readIniFile(os.path.join(self.appDir,'configuration.ini'))
		except Exception as e:
			print(e)
			sys.exit("Cannot read actools config file. Exiting") 
		self.sevenzipexec = self.properAbsPath(self.readMandatoryConfigField(configIniFile, '7ZIP_EXEC'))
		self.acpath = self.properAbsPath(self.readMandatoryConfigField(configIniFile, 'ASSETTOCORSA_PATH'))
		self.acmodspath = self.properAbsPath(self.readMandatoryConfigField(configIniFile, 'MODS_PATH'))
		self.quickbmsexec = self.readMandatoryConfigField(configIniFile, 'QUICKBMS_EXE')
		if self.quickbmsexec != None:
			self.quickbmsexec = self.properAbsPath(self.quickbmsexec)
		if not os.path.isfile(self.quickbmsexec):
			self.quickbmsexec = None
		
		if not os.path.isfile(self.sevenzipexec):
			sys.exit("Cannot find 7zip executable. Exiting") 
		#if not os.path.isdir(self.acpath):
		#	sys.exit("Cannot find Assetto Corsa install folder. Exiting") 

		argsparser = argparse.ArgumentParser(description='Build/clean Assetto Corsa mods from mods archives or folders')
		argsparser.add_argument('-g','--guess', help='Try to guess what is the file given as parameter and process it (an archive, a mod, a track or a car folder)', required=False)
		argsparser.add_argument('-da','--dont_archive', action='store_true', help='Don''t generate archives for mods. IT will only create/update json files if requested', required=False)
		argsparser.add_argument('-u','--update_mod_url', action='store_true', help='Generate the meta_data.json needed for acServer or update ui_car.json', required=False)
		argsparser.add_argument('-act','--add_csp_tags', action='store_true', help='Add rainfx, weatherfx and grassfx tags to tracks if they have these specifics configs', required=False)
		argsparser.add_argument('-f','--force_override', action='store_true', help='If an archive already exists in the destination folder, it will be overriden, no matter the dates', required=False)
		argsparser.add_argument('-s','--skip_kunos_mods', action='store_true', help='Skip kunos mods when using #all for tracks or cars', required=False)
		argsparser.add_argument('-o','--override_archives', action='store_true', help='If an archive already exists in the destination folder, it will be overriden if the mod has a newer file than the archive to override', required=False)
		argsparser.add_argument('-tu','--track_url_prefix', help='The URL prefix to write into the acServer meta_data.json file for tracks, for the url field', required=False)
		argsparser.add_argument('-cu','--car_url_prefix', help='The URL prefix to write into the acServer meta_data.json file for cars, for the url field', required=False)
		argsparser.add_argument('-td','--tracks_destination', help='If specified, the generated archives will be generated here instead of the current dir', required=False)
		argsparser.add_argument('-cd','--cars_destination', help='If specified, the generated archives will be generated here instead of the current dir', required=False)
		argsparser.add_argument('-t','--tracks', help='The name of the tracks to archive from the assetto corsa install dir. If the value is #all, it will archive all the tracks.', required=False)
		argsparser.add_argument('-c','--cars', help='The name of the tracks to archive from the assetto corsa install dir. If the value is #all, it will archive all the cars.', required=False)
		argsparser.add_argument('-a','--archive', help='The path to a mod archive to transform to a good mod structure that can be enabled/disabled by Content Manager', required=False)
		argsparser.add_argument('-x','--clean', action='store_true', help='Remove from your assetto corsa content, any invalid track or car (meaning without ui information for cars, or less than 2 dirs for tracks)', required=False)
		argsparser.add_argument('-ft','--find_tracks_by_tags', help='Find tracks with the specified tags and write then in the std output', required=False)
		argsparser.add_argument('-fc','--find_cars_by_tags', help='Find cars with the specified tags and write then in the std output', required=False)

		args = vars(argsparser.parse_args())

		self.updateModUrlForAcServer = self.argValueOrFalse(args, 'update_mod_url')
		self.addCspTags = self.argValueOrFalse(args, 'add_csp_tags')
		self.forceOverride = self.argValueOrFalse(args, 'force_override')
		self.skipKunosMods = self.argValueOrFalse(args, 'skip_kunos_mods')
		self.dontArchive = self.argValueOrFalse(args, 'dont_archive')
		self.clean = self.argValueOrFalse(args, 'clean')
		self.overrideArchives = self.argValueOrFalse(args, 'override_archives')
		self.trackDownloadUrlPrefix = self.argValueOrNone(args, 'track_url_prefix')
		self.carDownloadUrlPrefix = self.argValueOrNone(args, 'car_url_prefix')
		self.tracksDestination = self.argPathOrNone(args, 'tracks_destination')
		self.findTracksByTags = self.argPathOrNone(args, 'find_tracks_by_tags')
		self.findCarsByTags = self.argPathOrNone(args, 'find_cars_by_tags')
		self.carsDestination = self.argPathOrNone(args, 'cars_destination')
		self.tracksToProcess = self.argValueOrNone(args, 'tracks')
		self.carsToProcess = self.argValueOrNone(args, 'cars')
		self.archiveToProcess = self.argValueOrNone(args, 'archive')
		self.guessToProcess = self.argValueOrNone(args, 'guess')

		if self.tracksDestination == None or self.tracksDestination == "":
			self.tracksDestination = os.getcwd()
		else:
			self.tracksDestination = self.properAbsPath(self.tracksDestination)
			
		if self.carsDestination == None or self.carsDestination == "":
			self.carsDestination = os.getcwd()
		else:
			self.carsDestination = self.properAbsPath(self.carsDestination)

		if self.archiveToProcess != None:
			self.archiveToProcess = self.properAbsPath(self.archiveToProcess)

		if self.guessToProcess != None:
			self.guessToProcess = self.properAbsPath(self.guessToProcess)
			if not os.path.exists(self.guessToProcess):
				sys.exit("Cannot find file to process. Exiting") 