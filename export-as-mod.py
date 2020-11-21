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


def processMod(paramsToUse, modTool, modsToProcess):
	if modsToProcess != None and modsToProcess.strip() != "":
		if modsToProcess == "#all":
			modTool.packAllMods(paramsToUse.modsDestDir, paramsToUse.createAcServerMetatadaFile, paramsToUse.overrideExistingArchives, paramsToUse.downloadUrlPrefix, paramsToUse.acpath)
		else:
			for mod in modsToProcess.split(","):
				modTool.packMod(mod, paramsToUse.modsDestDir, paramsToUse.createAcServerMetatadaFile, paramsToUse.overrideExistingArchives, paramsToUse.downloadUrlPrefix, paramsToUse.acpath)
	

paramsToUse = params.Params()
paramsToUse.checkEnv()
processMod(paramsToUse, tracks.TrackTools(paramsToUse.acpath, paramsToUse.sevenzipexec), paramsToUse.tracksToProcess)
processMod(paramsToUse, cars.CarTools(paramsToUse.acpath, paramsToUse.sevenzipexec), paramsToUse.carsToProcess)
