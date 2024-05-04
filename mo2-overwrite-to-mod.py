import os
import shutil 
from actools import archives
from actools import common

from actools import params

def recursive_copy(src, dst):
	if os.path.isdir(src):
		if not os.path.exists(dst):
			shutil.copytree(src, dst)
		else:
			for item in os.listdir(src):
				s = os.path.join(src, item)
				d = os.path.join(dst, item)
				recursive_copy(s,d)
	elif os.path.isfile(src):
		if not os.path.exists(dst):
			shutil.copy2(src, dst)
		else:
			print("ignoring copy of exsiting file" + src)

mo2CategoriesConfig = {}
def initmo2CategoriesConfig(categoriesDat):
	fileCat = open(categoriesDat, 'r')
	lines = fileCat.readlines()
	for line in lines:
		lineArray = line.strip().split('|')
		mo2CategoriesConfig[lineArray[0]] = lineArray[1]


def readMO2Category(metaIniFile):
	cats = []
	if os.path.isfile(metaIniFile):
		meta = common.readIniFile(metaIniFile)
		if meta.has_section('General'):
			if meta.has_option('General', 'category'):
				categoriesIntStr = meta.get('General', 'category')
				categoriesIntStr = categoriesIntStr.replace('"', '')
				for catInt in categoriesIntStr.split(","):
					catInt = catInt.replace(',', '')
					if catInt != None and catInt in mo2CategoriesConfig:
						cats.append(mo2CategoriesConfig[catInt])
	if len(cats) == 0:
		print("cannot find MO2 category for meta file " + metaIniFile)
	return cats

def main():
	paramsToUse = params.Params(os.path.dirname(os.path.realpath(__file__)))
	paramsToUse.checkEnv()
	overwriteDir = os.path.join(paramsToUse.acmodspath, "../overwrite")
	
	initmo2CategoriesConfig(os.path.join(paramsToUse.acmodspath, "../categories.dat"))
	# read all tracks and cars in mods
	tracks = {}
	cars = {}
	mo2Category = {}
	mods = os.listdir(paramsToUse.acmodspath)
	index = 0
	for mod in mods:
		tracksDir = os.path.join(paramsToUse.acmodspath, mod, "content", "tracks")
		carsDir = os.path.join(paramsToUse.acmodspath, mod, "content", "cars")
		if os.path.isdir(tracksDir):
			for trackname in os.listdir(tracksDir):
				trackDir = os.path.join(tracksDir, trackname)
				if not archives.isTrack(trackDir):
					#print("Warning, ignoring track dir " + trackDir + " because it's not a track")
					pass
				elif "Track skin - " in mod or "Track extension - " in mod:
					#print("Warning, ignoring track dir " + trackDir + " because it has skin or extension in the mod name"
					pass
				else:
					if trackname in tracks:
						print("Error processing " + trackDir + ", track " + trackname + " already found here: " + tracks[trackname])
						tracks.pop(trackname)
					else:
						tracks[trackname] = trackDir
						archives.fixTrackTags(trackDir, readMO2Category(os.path.join(paramsToUse.acmodspath, mod, "meta.ini")))
		if os.path.isdir(carsDir):
			for carname in os.listdir(carsDir):
				carDir = os.path.join(carsDir, carname)
				if archives.isCar(carDir):
					if carname in cars:
						print("Error processing " + carDir + ", car " + carname + " already found here:" + cars[carname])
						cars.pop(carname)
					else:
						cars[carname] = carDir
						archives.fixCarTags(carDir, readMO2Category(os.path.join(paramsToUse.acmodspath, mod, "meta.ini")))
						index += 1

	tracksOverwriteDir = os.path.join(overwriteDir, "content", "tracks")
	carsOverwriteDir = os.path.join(overwriteDir, "content", "cars")
	for trackname in os.listdir(tracksOverwriteDir):
		if trackname in tracks:
			recursive_copy(os.path.join(tracksOverwriteDir, trackname), tracks[trackname])
		shutil.rmtree(os.path.join(tracksOverwriteDir, trackname))
	for carname in os.listdir(carsOverwriteDir):
		if carname in cars:
			recursive_copy(os.path.join(carsOverwriteDir, carname), cars[carname])
		shutil.rmtree(os.path.join(carsOverwriteDir, carname))

main()