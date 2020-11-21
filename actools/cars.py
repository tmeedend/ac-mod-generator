import tempfile
import os
from actools import common
from actools import mods
from actools import fonts

from urllib.parse import urlparse

class CarTools(mods.ModTools):

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
        filesArray.extend(fonts.find(acpath, modId))
        return filesArray