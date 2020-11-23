import os
import tempfile
from actools import common
import shutil
import ntpath
def findLongestPrefix(m):
    if not m: return ''
    s1 = min(m)
    s2 = max(m)
    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]
    return s1

def findModName(finalModeDir, originalArchiveName):
    carslist = os.listdir(os.path.join(finalModeDir, 'content', 'cars'))
    tracklist =  = os.listdir(os.path.join(finalModeDir, 'content', 'tracks'))
    carsNumber = len(carslist)
    tracksNumber = len(tracklist)
    if carsNumber > 0 and tracksNumber > 0:
        # we cannot find a descent archive name, return the original name
        return originalArchiveName
    if carsNumber > 0:
        if carsNumber == 1:
            return extractCarArchiveName()
        else
            return findLongestPrefix(carslist)

    elif tracksNumber > 0:
        if tracksNumber == 1:
            return extractTrackArchiveName()
        else
            return findLongestPrefix(tracklist)
def isMod(dir):
    for filename in os.listdir(dir):
        file = os.path.join(dir, filename)
        if os.path.isdir(file) and filename == 'content':
            return True
    return False 

def isTrack(dir):
    if os.path.isfile(os.path.join(dir, 'ui', 'ui_track.json')):
        return True
    for layout in os.listdir(os.path.join(dir, 'ui')):
        if os.path.isdir(os.path.join(dir, 'ui', layout)):
            mod_ui_json = os.path.join(dir, 'ui', layout, 'ui_track.json')
            if os.path.isfile(mod_ui_json):
                return True
    return False


def isCar(dir):
    return os.path.isfile(os.path.join(dir, 'ui', 'ui_car.json'))

def appendMod(dir, newModDir, type):
    if type == 'MOD':
        for subdirname in os.listdir(dir):
            subdir = os.path.join(dir, subdirname)
            shutil.move(subdir,newModDir)
    elif  type == 'TRACK':
        tracksPath = os.path.join(newModDir, 'content', 'tracks')
        os.makedirs(tracksPath)
        shutil.move(dir,tracksPath)
    elif  type == 'CAR':
        carsPath = os.path.join(newModDir, 'content', 'cars')
        os.makedirs(carsPath)
        shutil.move(dir,carsPath)

def transformToValidMod(params):
    if not params.archiveToProcess == None:
        if not os.path.isfile(params.archiveToProcess ):
            print("Cannot find archive " +  params.archiveToProcess)
            return

    workdir = tempfile.mkdtemp()
    common.unzipFileToDir(params.sevenzipexec, params.archiveToProcess, workdir)
    newModDir = tempfile.mkdtemp()
    if isMod(workdir):
        appendMod(workdir, newModDir, 'MOD')
    else:
        for filename in os.listdir(workdir):
            file = os.path.join(workdir, filename)
            if isMod(file):
                appendMod(file, newModDir, 'MOD')
            elif isTrack(file):
                appendMod(file, newModDir, 'TRACK')
            elif isCar(file):
                appendMod(file, newModDir, 'CAR')
    finalArchiveName = findModName(newModDir, ntpath.basename(params.archiveToProcess))
    common.zipFileToDir(params.sevenzipexec, newModDir, os.path.join(os.getcwd(), finalArchiveName), None, params.forceOverride, None)
                