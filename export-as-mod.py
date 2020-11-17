import os
import subprocess
import sys
import tempfile
import json
import urllib.parse

sevenzipexec = 'C:' + os.sep + 'Program Files' + os.sep + '7-Zip' + os.sep + '7z.exe'
acpath = 'D:' + os.sep + 'Program Files (x86)' + os.sep + 'Steam' + os.sep + 'steamapps' + os.sep + 'common' + os.sep + 'assettocorsa'
trackToProcess = ''
trackModsDestDir = 'D:\\Dropbox\\Assetto Mods\\Tracks'
createAcServerMetatadaFile = True
acServerDownloadUrlPrefix="http://37.187.124.217/dP1dG9mT5uV0eE0jI6hM7qF0rK2aK9bT/ac-mods/"
includeAcServerMetatadaFileInArchive=False

def createTrackMetaData(trackDir, archiveName):
	metadataFilePath = trackDir + os.sep + "ui" + os.sep + "meta_data.json"
	if os.path.isfile(metadataFilePath):
		metadatafile = open(metadataFilePath, "w")
	else:
		metadatafile = open(metadataFilePath, "x")
	metadatafile.write('{\n')
	metadatafile.write('"downloadURL": "' + acServerDownloadUrlPrefix + urllib.parse.quote(archiveName) + '",\n')
	metadatafile.write('"notes": "",\n')
	metadatafile.write('}\n')
def checkEnv():
	if not os.path.isfile(sevenzipexec):
		sys.exit("Cannot find 7zip executable. Exiting") 
	if not os.path.isdir(acpath):
		sys.exit("Cannot find Assetto Corsa executable. Exiting") 


def zipFileToDir(workingDirectory, archiveFile, listfilename):
	origWD = os.getcwd() # remember our original working directory
	try:
		os.chdir(workingDirectory) 
		if os.path.isfile(archiveFile):
			print("Removing old archive file " + archiveFile)
			os.remove(archiveFile)
		archiveCmd = sevenzipexec + " a " + archiveFile + " -spf @" + listfilename
		if not includeAcServerMetatadaFileInArchive:
			archiveCmd = archiveCmd + " -xr!meta_data.json"
		print('executing ' + archiveCmd)
		subprocess.Popen(archiveCmd).communicate()
	except:
		print("Error while archiving mod") 
	finally:
		os.chdir(origWD) # get back to our original working directory 
		
def cleanName(name):
	remove_punctuation_map = dict((ord(char), None) for char in '\/*?:"<>|')
	return name.translate(remove_punctuation_map)

def packTrack(track):
	print('generating mod for track ' + track)
	workdir = tempfile.mkdtemp()
	trackspath = acpath + os.sep + 'content' + os.sep + 'tracks'
	listfilename = workdir + os.sep + track + ".txt"
	listfile = open(listfilename, "x")
	listfile.write('content' + os.sep + 'tracks' + os.sep + track + '\n')

	# read version
	trackPath = trackspath + os.sep + track
	track_ui_json = trackPath + os.sep +'ui' + os.sep + 'ui_track.json'
	
	try:
		jsonFile = json.loads(open(track_ui_json).read())
	except:
		print("Cannot parse ui_track.json for track " + track)
		return
	trackVersion = jsonFile['version']
	trackAuthor = jsonFile['author']
	trackVersionName = track
	if not trackVersion == None:
		trackVersionName += " " + trackVersion
	if not trackAuthor == None:
		trackVersionName += " by " + trackAuthor
	trackVersionName = cleanName(trackVersionName)
	print("archive name is " + trackVersionName)


	# create structure
	# os.makedirs(workdir + '/' + trackVersionName + '/content/tracks/')
	# os.symlink(trackspath + '/' + track, workdir + '/' + trackVersionName + '/content/tracks/' + track)

	# extension config file
	extensionFoncigTrackFile =  'extension' + os.sep + 'config' + os.sep + 'tracks' + os.sep + track + '.ini'
	if os.path.isfile(acpath + os.sep + extensionFoncigTrackFile):
		listfile.write(extensionFoncigTrackFile + '\n')
	listfile.close()

	# zip the track
	archiveFile = '"' + trackModsDestDir + os.sep + trackVersionName + '.7z"'
	zipFileToDir(acpath, archiveFile, listfilename)
	os.remove(listfilename)
	if createAcServerMetatadaFile:
		createTrackMetaData(trackPath, trackVersionName)

def packAllTracks():
	kunosTracks = {"ks_barcelona", "ks_black_cat_county", "ks_brands_hatch", "ks_drag", "ks_highlands", "ks_laguna_seca", "ks_monza66", "ks_nordschleife", "ks_nurburgring", "ks_red_bull_ring", "ks_silverstone", "ks_silverstone1967", "ks_vallelunga", "ks_zandvoort", "magione", "monza", "mugello", "spa", "trento-bondone", "drift", "imola"}
	trackspath = acpath + os.sep + 'content' + os.sep + 'tracks'
	tracks = os.listdir(trackspath)
	for track in tracks:
		if not track in kunosTracks:
			packTrack(track)

def main():
	checkEnv()
	if trackToProcess is None or trackToProcess == "":
		packAllTracks()
	else:
		packTrack(trackToProcess)

main()