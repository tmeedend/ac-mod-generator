import glob, os
import tempfile
import stat
from actools import common
import shutil
import ntpath
from actools import tracks
from actools import cars


def findModName(finalModeDir, originalArchiveName, title = False):
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
        if title:
            return (cars.CarTools(None, None)).extractModArchiveTitle(os.path.join(carsDir, carslist[0]))
        else:
            return (cars.CarTools(None, None)).extractModArchiveName(os.path.join(carsDir, carslist[0]))

    elif tracksNumber > 0:
        if tracksNumber == 1:
            if title:
                return (tracks.TrackTools(None, None)).extractModArchiveTitle(os.path.join(tracksDir, tracklist[0]))
                return 
            else:
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

def del_rw(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)
    os.unlink(name)

def installMods(params, newModDir, originalName):
    soundModsFound = False
    for subdirname in os.listdir(newModDir):
        if str.startswith(subdirname, 'sound_'):
            print("\tInstalling sound mod " + subdirname)
            shutil.move(os.path.join(newModDir, subdirname), params.acmodspath)
            soundModsFound = True
    if soundModsFound == False:
        finalModName =  findModName(newModDir, originalName, True)
        modInstallDir = os.path.join(params.acmodspath, finalModName)
        if(os.path.isdir(modInstallDir)):
            print('Replacing mod ' + finalModName + ' because it already exists in ' + params.acmodspath)
            if os.path.isdir(os.path.join(modInstallDir, "content")):
                shutil.rmtree(os.path.join(modInstallDir, "content"), onerror=del_rw)
            if os.path.isdir(os.path.join(modInstallDir, "extension")):
                shutil.rmtree(os.path.join(modInstallDir, "extension"), onerror=del_rw)
            if os.path.isdir(os.path.join(modInstallDir, "system")):
                shutil.rmtree(os.path.join(modInstallDir, "system"), onerror=del_rw)
        os.makedirs(modInstallDir, exist_ok= True)
        # move all files into the install mod dir
        file_names = os.listdir(newModDir)
        for file_name in file_names:
            newfile = os.path.join(newModDir, file_name)
            if newModDir[0] == modInstallDir[0]:
                shutil.move(newfile, modInstallDir)
            else:
                common.copytree(newfile, modInstallDir)
                #shutil.rmtree(newfile, onerror=del_rw)

def transformToValidMod(params, archiveToProcess):
    if not archiveToProcess == None:
        if not os.path.isfile(archiveToProcess ):
            print("Cannot find archive " +  archiveToProcess)
            return
    else:
        return
    # create a tmp work dir and unzip the archive to process inside
    workdir = tempfile.mkdtemp()
    print("Unzipping archive to " + workdir)
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


def fixTrackTags(modDir, mo2categories):
    tagsToRemove = ['1966', '1988', '1994', '2001', '2021', 'acc', 'bollene','carlo','canada','carrera.4','chicago','chiquifreaky',"chq",'dragon','euroracers','exeqt0r','imola',
    'interlagos','fat-alfie','germany','gpl','hockenheim', 'lemax',
    'mod','monte','monaco','moscow','pau', 'permanent racing circuit', 'quebec','rainmaker', 'remake','rmi','san francisco', "saudi arabia",
    'superstage', 'shibuya', 'trail', 'tyrone','vesubie', "yeda", "yokohama"]
    if mo2categories == None:
        mo2categories = []
    layouts = []
    layoutsOk = []
    layouts.append(os.path.join(modDir, "ui", "ui_track.json"))

    for file in os.listdir(os.path.join(modDir, "ui")):
        layouts.append(os.path.join(modDir, "ui", file, "ui_track.json"))

    for layoutJsonFile in layouts:
        if os.path.isfile(layoutJsonFile):
            try:
                jsonData = common.parseJson(layoutJsonFile)
            except Exception as e: 
                print(e)
                print ("Cannot load ui_track.json to fix track for json file " + layoutJsonFile)
                return
            layoutTags = jsonData['tags'] 
            modUpdatedTagsSet = set()
            for tag in layoutTags:
                tag = tag.lower()
                if not tag in tagsToRemove:
                    if tag == 'freeroam':
                        modUpdatedTagsSet.add('#freeroam')
                    elif tag == '#circuit':
                        modUpdatedTagsSet.add('circuit')
                    elif tag == 'country':
                        modUpdatedTagsSet.add('country-side')
                    elif tag == '24h' or tag == 'sebring':
                        modUpdatedTagsSet.add('endurance')
                    elif tag == 'grand prix':
                        modUpdatedTagsSet.add('gp')
                    elif tag == 'city':
                        modUpdatedTagsSet.add('street')
                    elif tag == 'dockland':
                        modUpdatedTagsSet.add('docks')
                    elif tag == 'formula 1':
                        modUpdatedTagsSet.add('f1')
                    elif tag == 'historic gp':
                        modUpdatedTagsSet.add('historic')
                        modUpdatedTagsSet.add('gp')
                    elif tag == 'p2p':
                        modUpdatedTagsSet.add('a2b')
                    elif tag == 'drift':
                        modUpdatedTagsSet.add('#drift')
                    elif tag == 'hillclimb' or tag == 'hill climb':
                        modUpdatedTagsSet.add('hillclimb')
                        modUpdatedTagsSet.add('a2b')
                        modUpdatedTagsSet.add('#rally')
                    elif tag == 'rally' or tag == 'rallye' or tag == 'wrc' or tag == 'stage' or tag == 'speciale':
                        modUpdatedTagsSet.add('#rally')
                    elif tag == 'dirt3' or tag == 'fm7' or tag == 'grid' or tag == 'grid2' or tag == 'grid autosport' or tag == 'forza motorsport':
                        modUpdatedTagsSet.add('fictional')
                    else:
                        modUpdatedTagsSet.add(tag)
            modName = jsonData['name']
            
            for cat in mo2categories:
                if cat == 'Track - Rally':
                    modUpdatedTagsSet.add('#rally')
                elif cat == 'Track - Freeroam':
                    modUpdatedTagsSet.add('#freeroam')
                elif cat == 'Circuit - Endurance':
                    modUpdatedTagsSet.add('endurance')
                elif cat == 'Circuit - Vintage':
                    modUpdatedTagsSet.add('vintage')
                elif cat == 'Circuit - Drift':
                    modUpdatedTagsSet.add('#drift')

            modUpdatedTags= []
            # copy set in array
            for tag in modUpdatedTagsSet:
                modUpdatedTags.append(tag)

            jsonData.update({'tags':modUpdatedTags})
            try:
                with open(layoutJsonFile, "w") as jsonFile:
                    json.dump(jsonData, jsonFile, indent=2)
            except Exception as e: 
                print(e)
                print ("Cannot save new tags to fix track for mod " + modName)

def fixCarTags(modDir, mo2categories):
    metadataFilePath =  os.path.join(modDir, "ui", "ui_car.json")
    try:
        jsonData = common.parseJson(metadataFilePath)
    except Exception as e: 
        print(e)
        print ("Cannot load ui_car.json to fix car for mod " + modDir)
        return
    modTags = jsonData['tags']
    if mo2categories == None:
        mo2categories = []
    modName = jsonData['name']
    modNameLower = modName.lower()
    
    modClass = jsonData['class'].lower()
    modBrand =  jsonData['brand']

    ###### fix brand ######
    if "bayro" in modNameLower:
        modBrand = "BMW"
    elif "auriel" in modNameLower:
        modBrand = "Audi"
    elif "darche" in modNameLower:
        modBrand = "Porsche"
    elif "minardi" in modNameLower:
        modBrand = "Minardi"
    elif "bar "in modNameLower:
        modBrand = "Bar"

    modUpdatedTagsSet = set()
    # guess tags from name
    if modNameLower.__contains__('police'):
        modUpdatedTagsSet.add('police')
    if modNameLower.__contains__('taxi'):
        modUpdatedTagsSet.add('taxi')
    if modNameLower.__contains__('traffic'):
        modUpdatedTagsSet.add('#traffic')
    if modNameLower.__contains__('truck'):
        modUpdatedTagsSet.add('#truck')

    # modYear = jsonData['year']

    ###### fix class ######
    if modClass != 'race' and modClass != 'street':
        if modClass == 'racing' or modClass == 'grand prix' or modClass == 'dpi' or modClass == 'group 6 gen 1' or modClass == 'group 5 gen 3' or modClass == 'group 5' or modClass == 'cup' or modClass == 'gt' or modClass == 'ac legends' or modClass == 'f2':
            modClass = 'race'
        elif modClass == 'drift' or  modClass == 'street drift' :
            modUpdatedTagsSet.add('#drift')
        elif modClass == 'rally' or modClass == 'hillclimb' or modClass == 'pikespeak' or modClass == 'kit-car':
            modUpdatedTagsSet.add('#rally')
            modClass = 'race'
        elif modClass == 'stock' or modClass == 'tuning' or modClass == 'ev' or modClass == 'shutoko' or modClass == 'touge' or modClass == 'street/trackday' or modClass == 'tuned' or modClass == 'wangan':
            modClass = 'street'
        elif modClass == 'rally gr4':
            modUpdatedTagsSet.add('#rally')
            modUpdatedTagsSet.add('group 4')
            modClass = 'race'
        elif modClass == 'tcr':
            modUpdatedTagsSet.add('#tcr')
            modClass = 'race'
        elif modClass == 'wtcr':
            modUpdatedTagsSet.add('#wtcr')
            modClass = 'race'
        elif modClass == 'gt500':
            modUpdatedTagsSet.add('#gt500')
            modClass = 'race'
        elif modClass == 'dtm':
            modUpdatedTagsSet.add('#dtm')
            modClass = 'race'
        elif modClass == 'group 5':
            modClass = 'race'
        elif modClass == 'formula 3':
            modUpdatedTagsSet.add('#formula 3')
            modClass = 'race'
        elif modClass == 'prototype' or modClass == 'group c':
            modUpdatedTagsSet.add('prototype')
            modClass = 'race'
        elif modClass == 'traffic':
            modUpdatedTagsSet.add('#traffic')
            modClass = 'street'
        elif modClass == 'historic' or modClass == 'vintage':
            modUpdatedTagsSet.add('vintage')
            modClass = 'race'
        elif modClass == 'utility':
            modUpdatedTagsSet.add('#utility')
            modClass = 'street'
        else:
            print ("Warning, car " + modName + " has invalid class " + modClass)
    

    ###### fix tags ######
    tagsToRemove = ['1923','1.4 inline-4 8v', '5-speed', '300zx','718', '911', '993', '1973', '1990s', '#a1','#a5', 'a1', 'ap1', 'a2','a3dr', 'a5','alpine','amg',
     'audi','assettocorsamods', 'bmw', 'california','camaro', 'car','carrera','ceky perfomance','ceky performance','c-one','cayman', 'civic','dp', 'ddm','evo','e36','ek9','euro pack', 'evo4',
      'f5', 
    'fd2', 'france', 'fk 11','fiat',
    'germany','gts-r','gt+2.0', 'gue', 'great britain','gapplebees','gt3 rs','gtr','guerilla mods','honda','italy','ita','japan', 'koldo83', 'lambo','lms', 'ltk','legend', 'legends',
    'm4', 'm3', 'm power', 'mr', 'mrs', 'ma70', 'mod', 'mugen', 'n/a', 'nissan', 'nsx',
     'p.verdes','pm3dm','peugeot', 'public release', 'physics v3', 'porsche','prelude','r1',
    'rb25', 'r31', 'r32', 'r8', 'race', 'racing software', 'rollovers', 'romania','#rss', 'r1', 'rs', 'rsr',
    'rss', 's1', 's3.0','s15','scorpion', 'sin', 'sl63', 'stock', 'street',  'supra', 'silvia', 'singer', 'shutoko','s2000','skyline','toyota','tm-modding', 'track', 'ttrs', 'type r', 'usa', 'vantage',
    'x-bow', 'wip', 'zzw30']
    for tag in modTags:
        tag = tag.lower()
        if not tag in tagsToRemove:
            if tag == 'rally' or tag == 'rallye' or tag == '#rallye' or tag == 'hillclimb' or tag == 'wrc' or tag == '#rally wrc':
                modUpdatedTagsSet.add('#rally')
            elif tag == 'lmp1':
                modUpdatedTagsSet.add('#lmp1')
                modUpdatedTagsSet.add('prototype')
                modUpdatedTagsSet.add('endurance')
            elif tag == 'lmp2':
                modUpdatedTagsSet.add('#lmp2')
                modUpdatedTagsSet.add('prototype')
                modUpdatedTagsSet.add('endurance')
            elif tag == 'lmp900':
                modUpdatedTagsSet.add('#lmp900')
                modUpdatedTagsSet.add('prototype')
                modUpdatedTagsSet.add('endurance')
            elif tag == 'lmgt':
                modUpdatedTagsSet.add('#lmgt')
                modUpdatedTagsSet.add('gt1')
                modUpdatedTagsSet.add('gt')
                modUpdatedTagsSet.add('vintage')
                modUpdatedTagsSet.add('endurance')
            elif tag == 'lmgtp':
                modUpdatedTagsSet.add('#lmgtp')
                modUpdatedTagsSet.add('prototype')
                modUpdatedTagsSet.add('endurance')
            elif tag == 'f1' or tag.startswith("formula 1") or tag.startswith("#formula 1"):
                modUpdatedTagsSet.add("#formula 1")
                modUpdatedTagsSet.add('openwheeler')
                modUpdatedTagsSet.add('singleseater')
            elif tag == 'f2' or tag.startswith("formula 2") or tag.startswith("#formula 2"):
                modUpdatedTagsSet.add("#formula 2")
                modUpdatedTagsSet.add('openwheeler')
                modUpdatedTagsSet.add('singleseater')
            elif tag == 'f3' or tag.startswith("formula 3") or tag.startswith("#formula 3"):
                modUpdatedTagsSet.add("#formula 3")
                modUpdatedTagsSet.add('openwheeler')
                modUpdatedTagsSet.add('singleseater')
            elif tag == 'formula ford':
                modUpdatedTagsSet.add('#formula ford')
            elif tag == 'btcc':
                modUpdatedTagsSet.add('#btcc')
            elif tag == 'dpi' or tag == '#dpi':
                modUpdatedTagsSet.add('dpi')
            elif tag == 'drm':
                modUpdatedTagsSet.add('#drm')
            elif tag == 'grand prix':
                modUpdatedTagsSet.add('gp')
            elif tag == 'lemans' or tag == 'le mans':
                modUpdatedTagsSet.add('endurance')
            elif tag == 'gra':
                modUpdatedTagsSet.add('#rally')
                modUpdatedTagsSet.add('group 3')
            elif tag == 'dtm':
                modUpdatedTagsSet.add('#dtm')
            elif tag == '#gte'or tag == 'gte' :
                modUpdatedTagsSet.add('#lm-gte')
                modUpdatedTagsSet.add('endurance')
            elif tag == 'gt2' or tag == '#gt2' :
                modUpdatedTagsSet.add('#gt2')
                modUpdatedTagsSet.add('endurance')
            elif tag == 'gt4':
                modUpdatedTagsSet.add('#gt4')
            elif tag == 'gt3':
                modUpdatedTagsSet.add('#gt3')
            elif tag == 'n-gt':
                modUpdatedTagsSet.add('#n-gt')
            elif tag == 'tcr':
                modUpdatedTagsSet.add('#tcr')
            elif tag == '#sgt500' or tag == 'jgtc' or tag == 'gt500':
                modUpdatedTagsSet.add('#gt500')
            elif tag == 'can-am' or tag == 'can am' or tag == '#can-am' or tag == '#can am':
                modUpdatedTagsSet.add('#can-am')
            elif tag == 'traffic':
                modUpdatedTagsSet.add('#traffic')
            elif tag == 'sport' or tag == 'roadsport'or tag == 'sportscar'or tag == 'sportcar':
                modUpdatedTagsSet.add('#sportscars')
            elif tag == 'open wheeler':
                modUpdatedTagsSet.add('openwheeler')
            elif tag == 'single seater':
                modUpdatedTagsSet.add('singleseater')
            elif tag == 'historic':
                modUpdatedTagsSet.add('vintage')
            elif tag == 'hothatch' or tag == 'hot hatchback':
                modUpdatedTagsSet.add('hatchback')
            elif tag == 'supercar' or tag == '#supercar':
                modUpdatedTagsSet.add('#supercars')
            elif tag == 'proto c' or tag == '#proto c' or tag == 'prototype c' or tag == 'group c' or tag == '#group c' or tag == '#prototypes grc'  or tag == '#group-c/3.5':
                modUpdatedTagsSet.add('#prototypes group c')
                modUpdatedTagsSet.add('prototype')
                modUpdatedTagsSet.add('endurance')
            elif tag == 'wangan' or tag == 'jdm':
                modUpdatedTagsSet.add('#jdm')
            else:
                modUpdatedTagsSet.add(tag)
        #else:
        #    print("ignoring tag " + tag)


    for cat in mo2categories:
        if cat == 'Car - BTCC':
            modUpdatedTagsSet.add('#btcc')
        if cat == 'Car - Rally':
            modUpdatedTagsSet.add('#rally')
        elif cat == 'Car - Cup and Misc':
            modUpdatedTagsSet.add('cup')
        elif cat == 'Car - GT500':
            modUpdatedTagsSet.add('#gt500')
        elif cat == 'Car - GT1':
            modUpdatedTagsSet.add('gt1')
        elif cat == 'Car - LMGT':
            modUpdatedTagsSet.add('#lmgt')
            modUpdatedTagsSet.add('gt1')
            modUpdatedTagsSet.add('gt')
            modUpdatedTagsSet.add('vintage')
            modUpdatedTagsSet.add('endurance')
        elif cat == 'Car - LMGTP':
            modUpdatedTagsSet.add('#lmgtp')
            modUpdatedTagsSet.add('prototype')
            modUpdatedTagsSet.add('endurance')
        elif cat == 'Car - LM-GTE':
            modUpdatedTagsSet.add('#lm-gte')
            modUpdatedTagsSet.add('endurance')
        elif cat == 'Car - N-GT':
            modUpdatedTagsSet.add('#n-gt')
        elif cat == 'Car - GT2':
            modUpdatedTagsSet.add('#gt2')
        elif cat == 'Car - GT3':
            modUpdatedTagsSet.add('#gt3')
        elif cat == 'Car - GT4':
            modUpdatedTagsSet.add('#gt4')
        elif cat == 'Car - Proto - LMP1':
            modUpdatedTagsSet.add('#lmp1')
            modUpdatedTagsSet.add('prototype')
            modUpdatedTagsSet.add('endurance')
        elif cat == 'Car - Proto - LMH':
            modUpdatedTagsSet.add('#lmh')
            modUpdatedTagsSet.add('prototype')
            modUpdatedTagsSet.add('endurance')
        elif cat == 'Car - Proto - LMP2':
            modUpdatedTagsSet.add('#lmp2')
            modUpdatedTagsSet.add('prototype')
            modUpdatedTagsSet.add('endurance')
        elif cat == 'Car - Road - Drift':
            modUpdatedTagsSet.add('#drift')
        elif cat == 'Car - Formula 1':
            modUpdatedTagsSet.add("#formula 1")
            modUpdatedTagsSet.add('openwheeler')
            modUpdatedTagsSet.add('singleseater')
        elif cat == 'Car - Indicar':
            modUpdatedTagsSet.add('openwheeler')
            modUpdatedTagsSet.add('singleseater')
            modUpdatedTagsSet.add('#indicar')
        elif cat == 'Car - Nascar':
            modUpdatedTagsSet.add('#nascar')
        elif cat == 'Car - Traffic':
            modUpdatedTagsSet.add('#traffic')
        elif cat == 'Car - Road - JDM Culture':
            modUpdatedTagsSet.add('#jdm')
        elif cat == 'Car - Proto Group C':
            modUpdatedTagsSet.add('#prototypes group c')
            modUpdatedTagsSet.add('prototype')
            modUpdatedTagsSet.add('endurance')
    
    modUpdatedTags= []
    # copy set in array
    for tag in modUpdatedTagsSet:
        modUpdatedTags.append(tag)

    jsonData.update({'tags':modUpdatedTags})
    jsonData.update({'class':modClass})
    jsonData.update({'brand':modBrand})
    try:
        with open(metadataFilePath, "w") as jsonFile:
            json.dump(jsonData, jsonFile, indent=2)
    except Exception as e: 
        print(e)
        print ("Cannot save new tags to fix car for mod " + modName)

def recursiveMoveModsToValidModDir(workdir, newModDir, currentDirName):
    # first we check if the first dir level is a mod
    if isTrack(workdir):
        appendMod(workdir, newModDir, 'TRACK')
    elif isCar(workdir):
        appendMod(workdir, newModDir, 'CAR')
    elif isCarSound(workdir):
        newSoundDir = os.path.join(newModDir, 'sound_' + currentDirName)
        appendMod(workdir, newSoundDir, 'SOUND')
    #elif isMod(workdir):
    #    appendMod(workdir, newModDir, 'MOD')

    #if not we try to find it in subdirs
    else:
        if os.path.isdir(workdir):
            for filename in os.listdir(workdir):
                file = os.path.join(workdir, filename)
                recursiveMoveModsToValidModDir(file, newModDir, filename)