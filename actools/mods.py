import tempfile
import os
import time
from actools import common
from actools import params
import urllib.parse
from abc import ABC

class ModTools(ABC):

    sevenzipexec = None
    includeAcServerMetatadaFileInArchive = False
    def __init__(self, acpath, sevenzipexec):
        self.sevenzipexec = sevenzipexec

    def modType(self): 
        pass

    def modFiles(self, modId):
        pass

    def isKunosMod(self, mod):
        pass

    def destination(self, params):
        pass
    def modDownloadUrlPrefix(self, params):
        pass  

    def createMetaDataFile(self, modDir, archiveName, urlPrefix, dir ):
        metadataFilePath = modDir + os.sep + "ui" + os.sep + "meta_data.json"
        if os.path.isfile(metadataFilePath):
            metadatafile = open(metadataFilePath, "w")
        else:
            metadatafile = open(metadataFilePath, "x")
        metadatafile.write('{\n')
        metadatafile.write('"downloadURL": "' + urlPrefix + urllib.parse.quote(archiveName) + '.7z",\n')
        metadatafile.write('"notes": ""\n')
        metadatafile.write('}\n')


    def packMod(self, mod, params, dir):
        print('generating mod for mod ' + mod)
        workdir = tempfile.mkdtemp()
        modspath = dir + os.sep + 'content' + os.sep + self.modType() + 's'
        listfilename = workdir + os.sep + mod + ".txt"

        # read version
        modPath = modspath + os.sep + mod
        mod_ui_json = modPath + os.sep +'ui' + os.sep + 'ui_' + self.modType() + '.json'
        
        try:
            if os.path.isfile(mod_ui_json):
                jsonFile = common.parseJson(mod_ui_json)
            else:
                layouts = os.listdir(modPath + os.sep +'ui')
                if len(layouts) == 0:
                    print("Cannot find ui_" + self.modType() + ".json for mod " + mod)
                    return
                mod_ui_json = modPath + os.sep +'ui' + os.sep + layouts[0] + os.sep +'ui_' + self.modType() + '.json'
                jsonFile = common.parseJson(mod_ui_json)

        except Exception as e:
            print("Cannot parse " + mod_ui_json + ": ")
            print(e)
            return
        modVersion = jsonFile['version'] if 'version' in jsonFile else None
        modAuthor = jsonFile['author'] if 'author' in jsonFile else None
        modVersionName = mod
        if not modVersion == None:
            modVersionName += " " + modVersion
        if not modAuthor == None:
            modVersionName += " by " + modAuthor
        modVersionName = common.cleanName(modVersionName)
        print("archive name is " + modVersionName)

        # create structure
        # os.makedirs(workdir + '/' + modVersionName + '/content/tracks/')

        archiveFile = self.destination(params) + os.sep + modVersionName + '.7z'
        override=False
        if(params.forceOverride):
            override = True
        elif params.overrideArchives:
            if os.path.isfile(archiveFile):
                archiveDate = os.path.getctime(archiveFile)
                modNewestDate = common.getNewestFile(modPath)
                if( modNewestDate > archiveDate):
                    override = True
                    print("mod date is newer than archive date which is %s" % time.ctime(archiveDate))
                else:
                    print("Skipping archive override because mod date is older than archive date which is %s" % time.ctime(archiveDate))


        listfile = open(listfilename, "x")

        for fileToZip in self.modFiles(mod):
            if os.path.isfile(dir + os.sep + fileToZip) or os.path.isdir(dir + os.sep + fileToZip):
                listfile.write(fileToZip + '\n')    
        listfile.close()

        # zip the mod
        if not self.includeAcServerMetatadaFileInArchive:
            common.zipFileToDir(self.sevenzipexec, dir, archiveFile, listfilename, override, "meta_data.json")
        else:
            common.zipFileToDir(self.sevenzipexec, dir, archiveFile, listfilename, override, None)
        os.remove(listfilename)
        if params.createAcServerMetatadaFile:
           self.createMetaDataFile(modPath, modVersionName, self.modDownloadUrlPrefix(params), dir)

    def packAllMods(self, params, dir):
        modspath = dir + os.sep + 'content' + os.sep + self.modType() + 's'
        mods = os.listdir(modspath)
        for mod in mods:
            if not self.isKunosMod(mod):
                self.packMod(mod, params, dir)


