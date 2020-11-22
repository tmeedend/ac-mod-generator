import os
import subprocess
import sys
import tempfile
import json
import argparse

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
	

paramsToUse = params.Params()
paramsToUse.checkEnv()
processMod(paramsToUse, tracks.TrackTools(paramsToUse.acpath, paramsToUse.sevenzipexec), paramsToUse.tracksToProcess)
processMod(paramsToUse, cars.CarTools(paramsToUse.acpath, paramsToUse.sevenzipexec), paramsToUse.carsToProcess)
archives.transformToValidMod(paramsToUse)
# verifier les / a la fin des chemins et les enlever si besoin
# modFiles : vérifier dans cette méthode si les fichiers existent
# chemins mis en paramètre : vérifier qu'ils existent
# mod a pack  : verifier qu'il existe
# shaders spéciaaux cf shutoko
# rss formula  rss2 v6 : cm_texture.lua il y a des fonts dedans