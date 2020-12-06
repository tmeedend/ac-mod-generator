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

    def addCspTags(self, modId, acpath, modPath):
        pass

    def extractModArchiveName(self, modDir):
        mod = ntpath.basename(modDir)
        jsonFile = self.getUiJson(modDir)
        modVersion = jsonFile['version'] if 'version' in jsonFile else None
        modAuthor = jsonFile['author'] if 'author' in jsonFile else None
        modVersionName = self.modType() + " " + mod
        if not modVersion == None:
            modVersionName += " " + modVersion
        if not modAuthor == None:
            modVersionName += " by " + modAuthor
        return common.cleanName(modVersionName)

    def packMod(self, mod, params, dir):
        workdir = tempfile.mkdtemp()
        modspath = os.path.join(dir, 'content', self.modType() + 's')
        listfilename = os.path.join(workdir, mod + ".txt")
        modPath = os.path.join(modspath, mod)
        try:    
            modVersionName = self.extractModArchiveName(modPath)
        except Exception as e:
            print("\tCannot parse " + self.modType() + "_ui_json: ")
            print(e)
            return



        if params.updateModUrlForAcServer:
           self.updateModUrlForAcServer(modPath, modVersionName, self.modDownloadUrlPrefix(params), dir)

        if params.addCspTags:
            self.addCspTags(mod, dir, modPath)

        if params.dontArchive:
            return

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
                   #  print("\tmod date is newer than archive date which is %s" % time.ctime(archiveDate))
                else:
                    print("Skipping " + mod + " because mod date is older than archive date which is %s" % time.ctime(archiveDate))
                    return

        if os.path.isfile(archiveFile):
            if not override:
                print("Skipping mod " + mod + " because archive file " + archiveFile + " already exists.")
                return
        print('generating mod for ' + self.modType() + " " + mod)
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
        if not os.path.isdir(modspath):
            print("Error: Cannot find mod dir " + modspath)
            return
        mods = os.listdir(modspath)
        for mod in mods:
            if not self.isKunosMod(mod) or not params.skipKunosMods:
                try:
                    self.packMod(mod, params, dir)
                except Exception as e:
                    print("Error while generating mod " + mod)
                    print(e)
            else:
                print("Skipping kunos mod " + mod)


