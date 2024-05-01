import os
import ntpath

from actools import params


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
	overwriteDir = os.path.join(paramsToUse.acmodspath, "../overwrite")
	# read all tracks in mods
	tracks = {}
	mods = os.listdir(paramsToUse.acmodspath)
	for mod in mods:
		tracksDir = os.path.join(paramsToUse.acmodspath, mod, "content", "tracks")
		if os.path.isdir(tracksDir):
			for trackname in os.listdir(tracksDir):
				tracks[trackname] = os.path.join(tracksDir, trackname)
	print("printing found tracks")
	for key,value in tracks.items():
		print(key, ':', value)

main()