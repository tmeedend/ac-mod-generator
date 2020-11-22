import os
import tempfile
from actools import common
import shutil

def isMod(dir):
    for filename in os.listdir(dir):
        file = os.path.join(workdir, filename)
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

def appendMod(file, newModDir, type):
    if type == 'MOD':
        shutil.move(dir,newModDir)
    elif  type == 'TRACK':
        tracksPath = os.path.join(newModDir), 'content', 'tracks'
        os.makedirs(tracksPath)
        shutil.move(dir,tracksPath)
    elif  type == 'CAR':
        carsPath = os.path.join(newModDir), 'content', 'cars'
        os.makedirs(carsPath)
        shutil.move(dir,carsPath)

def transformToValidMod(params):
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
    common.zipFileToDir(params.sevenzipexec, newModDir, os.path.join(os.getcwd(), 'archive7z'), None, params.override, None)
                