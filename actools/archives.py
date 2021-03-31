import glob, os
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
        tracklist = os.listdir(tracksDir)
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
        if os.path.isdir(file) and (filename == 'content' or filename == 'extension'):
            return True
    return False 

def isTrack(dir):
    if not os.path.isdir(os.path.join(dir, 'ui')):
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

def isCarSound(dir):
    bankFiles = os.path.join(dir, '"*.bank"')
    if not os.path.isdir(dir) or len(glob.glob(bankFiles)) < 0:
        return False
    return os.path.isfile(os.path.join(dir, 'GUIDs.txt'))

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
    elif  type == 'SOUND':
        bankFile = glob.glob("*.bank")
        carname = ntpath.basename(bankFile[0])
        soundPath = os.path.join(newModDir, 'content', 'cars', carname, 'sfx')
        os.makedirs(soundPath, exist_ok= True)
        shutil.move(dir,soundPath)

def archiveValidMod(params, newModDir, originalName):
    finalModName =  findModName(newModDir, originalName)
    finalArchiveName = finalModName + '.7z'
    if os.access(os.getcwd(), os.W_OK):
        destArchive = os.path.join(os.getcwd(), finalArchiveName)
    else:
        destArchive = os.path.join(os.environ["HOMEPATH"], "Desktop", finalArchiveName)
    common.zipFileToDir(params.sevenzipexec, newModDir, destArchive, None, params.forceOverride, None)


def installMods(params, newModDir, originalName):
    soundModsFound = False
    for subdirname in os.listdir(newModDir):
        if str.startswith(subdirname, 'sound_'):
            print("\tInstalling sound mod " + subdirname)
            shutil.move(os.path.join(newModDir, subdirname), params.acmodspath)
            soundModsFound = True
    if soundModsFound == False:
        finalModName =  findModName(newModDir, originalName)
        modInstallDir = os.path.join(params.acmodspath, finalModName)
        if(os.path.isdir(modInstallDir)):
            print('Mod ' + finalModName + ' already exists in ' + params.acmodspath)
            return
        os.makedirs(modInstallDir, exist_ok= False)
        # move all files into the install mod dir
        file_names = os.listdir(newModDir)
        for file_name in file_names:
            shutil.move(os.path.join(newModDir, file_name), modInstallDir)


def transformToValidMod(params, archiveToProcess):
    if not archiveToProcess == None:
        if not os.path.isfile(archiveToProcess ):
            print("Cannot find archive " +  archiveToProcess)
            return
    else:
        return
    # create a tmp work dir and unzip the archive to process inside
    workdir = tempfile.mkdtemp()
    common.unzipFileToDir(params.sevenzipexec, archiveToProcess, workdir)
    
    # create a dir where we will put the mod once it has the good structure
    newModDir = tempfile.mkdtemp()

    # try to find mods in the extracted files
    recursiveMoveModsToValidModDir(workdir, newModDir, ntpath.basename(archiveToProcess))

    # if the generated mod dir is not empty, we have found a mod, we can process it
    if len(os.listdir(newModDir) ) > 0:
        installMods(params, newModDir, ntpath.basename(archiveToProcess))
    else:
        print("No mod found")

def recursiveMoveModsToValidModDir(workdir, newModDir, currentDirName):
    # first we check if the first dir level is a mod
    if isTrack(workdir):
        appendMod(workdir, newModDir, 'TRACK')
    elif isCar(workdir):
        appendMod(workdir, newModDir, 'CAR')
    elif isCarSound(workdir):
        newSoundDir = os.path.join(newModDir, 'sound_' + currentDirName)
        appendMod(workdir, newSoundDir, 'SOUND')
    elif isMod(workdir):
        appendMod(workdir, newModDir, 'MOD')

    #if not we try to find it in subdirs
    else:
        for filename in os.listdir(workdir):
            file = os.path.join(workdir, filename)
            recursiveMoveModsToValidModDir(file, newModDir, filename)