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

    def findModsWithTag(self, acpath, tagsToFind):
        pass

    def tagsInJson(self, file, tagsToFind):
        try:
            jsonData = common.parseJson(file)
            return len(set(jsonData['tags']) & set(tagsToFind)) > 0
        except:
            return False

    # extract the mod filename to generate from it's directory
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
        return common.cleanName(modVersionName, True)
    # extract the mod filename to generate from it's directory

    def extractModArchiveTitle(self, modDir):
        mod = ntpath.basename(modDir)
        jsonFile = self.getUiJson(modDir)
        modName = jsonFile['name'] if 'name' in jsonFile else mod.capitalize()
        modAuthor = jsonFile['author'] if 'author' in jsonFile else None
        modYear = jsonFile['year'] if 'year' in jsonFile else None
        modVersionName = self.modType().capitalize() + " - " + modName
        if not modYear == None:
            modVersionName += " - " + str(modYear)
        if not modAuthor == None:
            modVersionName += " (" + modAuthor + ")"
        return common.cleanName(modVersionName, False)

    def packMod(self, mod, params, dir):
        workdir = tempfile.mkdtemp()
        modspath = os.path.join(dir, 'content', self.modType() + 's')
        listfilename = os.path.join(workdir, mod + ".txt")
        modPath = os.path.join(modspath, mod)
        try:    
            modVersionName = self.extractModArchiveName(modPath)
        except Exception as e:
            print("\tCannot parse " + self.modType() + " " + mod + " _ui_json: ")
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
        if os.path.isfile(archiveFile):   
            if(params.forceOverride):
                override = True
                print('generating mod ' + self.modType() + " " + mod + " and force overriding old archive")
            elif params.overrideArchives:
                archiveDate = os.path.getmtime(archiveFile)
                modNewestDate = common.getNewestFile(modPath)
                if( modNewestDate > archiveDate):
                    override = True
                    print('generating mod ' + self.modType() + " " + mod + " because mod is newer than archive (%s > %s)" % (time.ctime(modNewestDate), time.ctime(archiveDate)))
                else:
                    # print("Skipping " + mod + " because mod date is older than archive date which is %s" % time.ctime(archiveDate))
                    return
            else:
                # print("Skipping mod " + mod + " because archive file " + archiveFile + " already exists.")
                return
        else:
            print('generating mod ' + self.modType() + " " + mod)

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


