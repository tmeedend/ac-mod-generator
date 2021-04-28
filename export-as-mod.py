import os
import subprocess
import sys
import tempfile
import json
import argparse
import ntpath

from actools import common
from actools import tracks
from actools import cars
from actools import params
from actools import archives
from actools import clean


def processMod(paramsToUse, modTool, modsToProcess):
	if modsToProcess != None and modsToProcess.strip() != "":
		if modsToProcess == "#all":
			modTool.packAllMods(paramsToUse, paramsToUse.acpath)
		else:
			if modsToProcess.startswith("tags:"):
				tags = modsToProcess.split("tags:")[1].split(',')
				mods = modTool.findModsWithTag(paramsToUse.acpath, tags)
			else:
				mods = modsToProcess.split(",")
			for mod in mods:
				if not modTool.isKunosMod(mod) or not paramsToUse.skipKunosMods:
					modTool.packMod(mod.strip(), paramsToUse, paramsToUse.acpath)
	

def main():
	paramsToUse = params.Params(os.path.dirname(os.path.realpath(__file__)))
	paramsToUse.checkEnv()
	
	# the guess param has been given
	if paramsToUse.guessToProcess != None:
		# if it's a file, then, we can process it if it's an archive
		if os.path.isfile(paramsToUse.guessToProcess):
			extension = os.path.splitext(paramsToUse.guessToProcess.lower())[1]
			if extension == ".rar" or extension == ".zip" or extension == ".7z":
				print("processing archive " + paramsToUse.guessToProcess)
				archives.transformToValidMod(paramsToUse, paramsToUse.guessToProcess)
				return
		# if, it's a dir we can process a car or track only if it's in an assetto corsa dir
		elif os.path.isdir(paramsToUse.guessToProcess):
			if not paramsToUse.acpath in paramsToUse.guessToProcess:
				sys.exit("Cannot process directory " + paramsToUse.guessToProcess + " because it's not in Assetto Corsa installation directory")
			print("processing directory " + paramsToUse.guessToProcess)
			if (archives.isTrack(paramsToUse.guessToProcess)):
				processMod(paramsToUse, tracks.TrackTools(paramsToUse.sevenzipexec, paramsToUse.quickbmsexec), os.path.basename(paramsToUse.guessToProcess))
				return
			elif (archives.isCar(paramsToUse.guessToProcess)):
				processMod(paramsToUse, cars.CarTools(paramsToUse.sevenzipexec, paramsToUse.quickbmsexec), os.path.basename(paramsToUse.guessToProcess))
				return
			elif (archives.isMod(paramsToUse.guessToProcess)):
				archives.archiveValidMod(paramsToUse, paramsToUse.guessToProcess, ntpath.basename(paramsToUse.guessToProcess))
				return
		else:
			print("Cannot guess what kind of mod this file is: " + paramsToUse.guessToProcess)
	else:
		trackTools = tracks.TrackTools(paramsToUse.sevenzipexec, paramsToUse.quickbmsexec)
		carTools = cars.CarTools(paramsToUse.sevenzipexec, paramsToUse.quickbmsexec)
		processMod(paramsToUse, trackTools, paramsToUse.tracksToProcess)
		processMod(paramsToUse, carTools, paramsToUse.carsToProcess)
		archives.transformToValidMod(paramsToUse, paramsToUse.archiveToProcess)
		if(paramsToUse.clean):
			if input("This will delete any car or track inside " + paramsToUse.acpath + " without a 'ui' directory. Are you sure? (y/n)") != "y":
				exit()
			clean.cleanCars(paramsToUse.acpath)
			clean.cleanTracks(paramsToUse.acpath)
		if paramsToUse.findTracksByTags  != None:
			foundTracks = trackTools.findModsWithTag(paramsToUse.acpath, paramsToUse.findTracksByTags.split(','))
			for track in foundTracks:
				print(track)
		if paramsToUse.findCarsByTags  != None:
			foundCars = carTools.findModsWithTag(paramsToUse.acpath, paramsToUse.findCarsByTags.split(','))
			for car in foundCars:
				print(car)

main()
# modFiles : vérifier dans cette méthode si les fichiers existent
# chemins mis en paramètre : vérifier qu'ils existent
# shaders spéciaux cf shutoko
