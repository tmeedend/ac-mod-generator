import tempfile
import os
import time
import ntpath
from actools import common
from actools import params
import urllib.parse
from abc import ABC

class ModTools(ABC):

    sevenzipexec = None
    quickbmsexec = None
    includeAcServerMetatadaFileInArchive = False
    def __init__(self, sevenzipexec, quickbmsexec):
        self.sevenzipexec = sevenzipexec
        self.quickbmsexec = quickbmsexec
    def modType(self): 
        pass

    def modFiles(self, modId, acpath):
        pass

    def isKunosMod(self, mod):
        pass

    def destination(self, params):
        pass
    
    def modDownloadUrlPrefix(self, params):
        pass  

    def updateModUrlForAcServer(self, modDir, archiveName, urlPrefix, dir ):
        pass
    
    def getUiJson(self, modDir):
        pass

    def extractModArchiveName(self, modDir):
        mod = ntpath.basename(modDir)
        jsonFile = self.getUiJson(modDir)
        modVersion = jsonFile['version'] if 'version' in jsonFile else None
        modAuthor = jsonFile['author'] if 'author' in jsonFile else None
        modVersionName = mod
        if not modVersion == None:
            modVersionName += " " + modVersion
        if not modAuthor == None:
            modVersionName += " by " + modAuthor
        return common.cleanName(modVersionName)

    def packMod(self, mod, params, dir):
        print('generating mod for mod ' + mod)
        workdir = tempfile.mkdtemp()
        modspath = os.path.join(dir, 'content', self.modType() + 's')
        listfilename = os.path.join(workdir, mod + ".txt")
        modPath = os.path.join(modspath, mod)
        try:    
            modVersionName = self.extractModArchiveName(modPath)
        except Exception as e:
            print("Cannot parse " + self.modType() + "_ui_json: ")
            print(e)
            return



        if params.updateModUrlForAcServer:
           self.updateModUrlForAcServer(modPath, modVersionName, self.modDownloadUrlPrefix(params), dir)

        archiveFile = os.path.join(self.destination(params), modVersionName + '.7z')
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

        for fileToZip in self.modFiles(mod, dir):
            if os.path.isfile(os.path.join(dir, fileToZip)) or os.path.isdir(os.path.join(dir, fileToZip)):
                listfile.write(fileToZip + '\n')    
        listfile.close()

        # zip the mod
        if not self.includeAcServerMetatadaFileInArchive:
            common.zipFileToDir(self.sevenzipexec, dir, archiveFile, listfilename, override, "meta_data.json")
        else:
            common.zipFileToDir(self.sevenzipexec, dir, archiveFile, listfilename, override, None)
        os.remove(listfilename)

    def packAllMods(self, params, dir):
        modspath = os.path.join(dir, 'content', self.modType() + 's')
        mods = os.listdir(modspath)
        for mod in mods:
            if not self.isKunosMod(mod):
                self.packMod(mod, params, dir)
            else:
                print("Skipping kunos mod " + mod)


