import tempfile
import os
from actools import common
from actools import mods
from urllib.parse import urlparse

class TrackTools(mods.ModTools):

    kunosTracks = {"ks_barcelona", "ks_black_cat_county", "ks_brands_hatch", "ks_drag", "ks_highlands", "ks_laguna_seca", "ks_monza66", "ks_nordschleife", "ks_nurburgring", "ks_red_bull_ring", "ks_silverstone", "ks_silverstone1967", "ks_vallelunga", "ks_zandvoort", "magione", "monza", "mugello", "spa", "trento-bondone", "drift", "imola"}

    def modType(self): 
        return "track"

    def isKunosMod(self, modId):
        return modId in self.kunosTracks
    
    def destination(self, params):
        return params.tracksDestination

    def modDownloadUrlPrefix(self, params):
        return params.trackDownloadUrlPrefix
        
    def modFiles(self, modId):
        return [
        # mod main folder
        'content' + os.sep + self.modType() + 's' + os.sep + modId,
        # extension config file
        'extension' + os.sep + 'config' + os.sep + self.modType()  + 's' + os.sep + modId + '.ini',
        # extension config file
        'extension' + os.sep + 'config' + os.sep + self.modType()  + 's' + os.sep + 'loaded' + os.sep + modId + '.ini',
        'extension' + os.sep + 'config' + os.sep + self.modType()  + 's' + os.sep + modId + '.ini.blm'
        ]