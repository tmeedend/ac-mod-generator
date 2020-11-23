import os
import tempfile
from actools import common
import shutil
import ntpath
from actools import tracks
from actools import cars


def findModName(finalModeDir, originalArchiveName):
    carsDir = os.path.join(finalModeDir, 'content', 'cars')
    if os.path.isdir(carsDir):
        carslist = os.listdir(carsDir)
    else:
        carslist = []

    tracksDir = os.path.join(finalModeDir, 'content', 'tracks')
    if os.path.isdir(tracksDir):
        tracklist = os.listdir()
    else:
        tracklist = []
    carsNumber = len(carslist)
    tracksNumber = len(tracklist)
    if carsNumber > 0 and tracksNumber > 0:
        # we cannot find a descent archive name, return the original name
        return os.path.splitext(originalArchiveName)[0]
    if carsNumber > 0:
        if carsNumber == 1:
            return (cars.CarTools(None, None)).extractModArchiveName(os.path.join(carsDir, carslist[0]))

    elif tracksNumber > 0:
        if tracksNumber == 1:
            return (tracks.TrackTools(None, None)).extractModArchiveName(os.path.join(tracksDir, tracklist[0]))

    return os.path.splitext(originalArchiveName)[0]

def isMod(dir):
    if not os.path.isdir(dir):
        return False
    for filename in os.listdir(dir):
        file = os.path.join(dir, filename)
        if os.path.isdir(file) and filename == 'content':
            return True
    return False 

def isTrack(dir):
    if not os.path.isdir(dir):
        return False
    if os.path.isfile(os.path.join(dir, 'ui', 'ui_track.json')):
        return True
    for layout in os.listdir(os.path.join(dir, 'ui')):
        if os.path.isdir(os.path.join(dir, 'ui', layout)):
            mod_ui_json = os.path.join(dir, 'ui', layout, 'ui_track.json')
            if os.path.isfile(mod_ui_json):
                return True
    return False


def isCar(dir):
    if not os.path.isdir(dir):
        return False
    return os.path.isfile(os.path.join(dir, 'ui', 'ui_car.json'))

def appendMod(dir, newModDir, type):
    if type == 'MOD':
        for subdirname in os.listdir(dir):
            subdir = os.path.join(dir, subdirname)
            shutil.move(subdir,newModDir)
    elif  type == 'TRACK':
        tracksPath = os.path.join(newModDir, 'content', 'tracks')
        os.makedirs(tracksPath, exist_ok= True)
        shutil.move(dir,tracksPath)
    elif  type == 'CAR':
        carsPath = os.path.join(newModDir, 'content', 'cars')
        os.makedirs(carsPath, exist_ok= True)
        shutil.move(dir,carsPath)

def transformToValidMod(params):
    if not params.archiveToProcess == None:
        if not os.path.isfile(params.archiveToProcess ):
            print("Cannot find archive " +  params.archiveToProcess)
            return

    workdir = tempfile.mkdtemp()
    common.unzipFileToDir(params.sevenzipexec, params.archiveToProcess, workdir)
    newModDir = tempfile.mkdtemp()
    foundSomething = False
    if isMod(workdir):
        appendMod(workdir, newModDir, 'MOD')
        foundSomething = True
    else:
        for filename in os.listdir(workdir):
            file = os.path.join(workdir, filename)
            if isMod(file):
                appendMod(file, newModDir, 'MOD')
                foundSomething = True
            elif isTrack(file):
                appendMod(file, newModDir, 'TRACK')
                foundSomething = True
            elif isCar(file):
                appendMod(file, newModDir, 'CAR')
                foundSomething = True
    if foundSomething:
        finalArchiveName = findModName(newModDir, ntpath.basename(params.archiveToProcess)) + '.7z'
        common.zipFileToDir(params.sevenzipexec, newModDir, os.path.join(os.getcwd(), finalArchiveName), None, params.forceOverride, None)
