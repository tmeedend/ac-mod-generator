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
	paramsToUse = params.Params()
	paramsToUse.checkEnv()
	if paramsToUse.guessToProcess != None:
		if os.path.isfile(paramsToUse.guessToProcess):
			extension = os.path.splitext(paramsToUse.guessToProcess.lower())[1]
			if extension == ".rar" or extension == ".zip" or extension == ".7z":
				archives.transformToValidMod(paramsToUse, paramsToUse.guessToProcess)
				return
		# we can process a car or track only if it's in assetto corsa dir
		elif os.path.isdir(paramsToUse.guessToProcess) and paramsToUse.acpath in paramsToUse.guessToProcess:
			if (archives.isTrack(paramsToUse.guessToProcess)):
				processMod(paramsToUse, tracks.TrackTools(paramsToUse.sevenzipexec, paramsToUse.quickbmsexec), os.path.basename(paramsToUse.guessToProcess))
				return
			elif (archives.isCar(paramsToUse.guessToProcess)):
				processMod(paramsToUse, cars.CarTools(paramsToUse.sevenzipexec, paramsToUse.quickbmsexec), os.path.basename(paramsToUse.guessToProcess))
				return
			elif (archives.isMod(paramsToUse.guessToProcess)):
				archives.archiveValidMod(paramsToUse, paramsToUse.guessToProcess, ntpath.basename(paramsToUse.guessToProcess))
				return
		print("Cannot guess what kind of mod this file is: " + paramsToUse.guessToProcess)
	else:
		processMod(paramsToUse, tracks.TrackTools(paramsToUse.sevenzipexec, paramsToUse.quickbmsexec), paramsToUse.tracksToProcess)
		processMod(paramsToUse, cars.CarTools(paramsToUse.sevenzipexec, paramsToUse.quickbmsexec), paramsToUse.carsToProcess)
		archives.transformToValidMod(paramsToUse, paramsToUse.archiveToProcess)

main()
# modFiles : vérifier dans cette méthode si les fichiers existent
# chemins mis en paramètre : vérifier qu'ils existent
# shaders spéciaux cf shutoko
# rss formula  rss2 v6 : cm_texture.lua il y a des fonts dedans
# trouver automatiquement le dossier AC avec ça : https://stackoverflow.com/questions/34090258/find-steam-games-folder
# ou https://stackoverflow.com/questions/56576172/how-to-get-path-of-installation-of-target-game-application-from-registry-when-in
