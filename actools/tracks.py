import tempfile
import os
from actools import common
from actools import mods
import urllib.parse

class TrackTools(mods.ModTools):

    kunosTracks = {"ks_barcelona", "ks_black_cat_county", "ks_brands_hatch", "ks_drag", "ks_highlands", "ks_laguna_seca", "ks_monza66", "ks_nordschleife", "ks_nurburgring", "ks_red_bull_ring", "ks_silverstone", "ks_silverstone1967", "ks_vallelunga", "ks_zandvoort", "magione", "monza", "mugello", "spa", "trento-bondone", "drift", "imola"}

    def updateModUrlForAcServer(self, modDir, archiveName, urlPrefix, dir ):
        metadataFilePath = os.path.join(modDir, "ui", "meta_data.json")
        if os.path.isfile(metadataFilePath):
            metadatafile = open(metadataFilePath, "w")
        else:
            metadatafile = open(metadataFilePath, "x")
        metadatafile.write('{\n')
        metadatafile.write('"downloadURL": "' + urlPrefix + urllib.parse.quote(archiveName) + '.7z",\n')
        metadatafile.write('"notes": ""\n')
        metadatafile.write('}\n')

    def modType(self): 
        return "track"

    def isKunosMod(self, modId):
        return modId in self.kunosTracks
    
    def destination(self, params):
        return params.tracksDestination

    def modDownloadUrlPrefix(self, params):
        return params.trackDownloadUrlPrefix

    def modFiles(self, modId, acpath):
        return [
        # mod main folder
        os.path.join( 'content', self.modType() + 's', modId),
        # extension config file
        os.path.join('extension','config', self.modType()  + 's', modId + '.ini'),
        # extension config file
        os.path.join('extension', 'config', self.modType()  + 's', 'loaded', modId + '.ini'),
        os.path.join('extension', 'config', self.modType()  + 's', modId + '.ini.blm')
        ]