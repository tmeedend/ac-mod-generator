import tempfile
import os
from actools import common
from actools import mods
from actools import fonts
from actools import drivers
import json
import urllib.parse

class CarTools(mods.ModTools):

    def updateModUrlForAcServer(self, modDir, archiveName, urlPrefix, dir ):
        metadataFilePath = modDir + os.sep + "ui" + os.sep + "ui_car.json"
        jsonData = common.parseJson(metadataFilePath)
        jsonData["downloadURL"] = urlPrefix + urllib.parse.quote(archiveName) + '.7z'
        with open(metadataFilePath, "w") as jsonFile:
            json.dump(jsonData, jsonFile, indent=2)

    def modType(self): 
        return "car"

    def kunosMods(self):
        return {"ks_abarth_595ss"}
    
    def destination(self, params):
        return params.carsDestination

    def modDownloadUrlPrefix(self, params):
        return params.carDownloadUrlPrefix

    def modFiles(self, modId, acpath):
        filesArray = [
        # mod main folder
        'content' + os.sep + self.modType() + 's' + os.sep + modId,
        # extension config file
        'extension' + os.sep + 'config' + os.sep + self.modType()  + 's' + os.sep + modId + '.ini',
        # extension config file
        'extension' + os.sep + 'config' + os.sep + self.modType()  + 's' + os.sep + 'loaded' + os.sep + modId + '.ini',
        'extension' + os.sep + 'config' + os.sep + self.modType()  + 's' + os.sep + modId + '.ini.blm'
        ]
        # filesArray.extend(fonts.find(acpath, modId))
        filesArray.extend(drivers.find(acpath, modId))
        return filesArray