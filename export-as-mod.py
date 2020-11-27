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


def processMod(paramsToUse, modTool, modsToProcess):
	if modsToProcess != None and modsToProcess.strip() != "":
		if modsToProcess == "#all":
			modTool.packAllMods(paramsToUse, paramsToUse.acpath)
		else:
			for mod in modsToProcess.split(","):
				modTool.packMod(mod.strip(), paramsToUse, paramsToUse.acpath)
	

def main():
	paramsToUse = params.Params(os.path.dirname(os.path.realpath(__file__)))
	paramsToUse.checkEnv()
	if paramsToUse.guessToProcess != None:
		if os.path.isfile(paramsToUse.guessToProcess):
			extension = os.path.splitext(paramsToUse.guessToProcess.lower())[1]
			if extension == ".rar" or extension == ".zip" or extension == ".7z":
				print("processing archive " + paramsToUse.guessToProcess)
				archives.transformToValidMod(paramsToUse, paramsToUse.guessToProcess)
				return
		# we can process a car or track only if it's in assetto corsa dir
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
		processMod(paramsToUse, tracks.TrackTools(paramsToUse.sevenzipexec, paramsToUse.quickbmsexec), paramsToUse.tracksToProcess)
		processMod(paramsToUse, cars.CarTools(paramsToUse.sevenzipexec, paramsToUse.quickbmsexec), paramsToUse.carsToProcess)
		archives.transformToValidMod(paramsToUse, paramsToUse.archiveToProcess)

main()
# modFiles : vérifier dans cette méthode si les fichiers existent
# chemins mis en paramètre : vérifier qu'ils existent
# shaders spéciaux cf shutoko
