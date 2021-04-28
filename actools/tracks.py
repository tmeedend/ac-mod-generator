import tempfile
import os
from actools import common
from actools import mods
import urllib.parse
import ntpath
import json
from array import array

class TrackTools(mods.ModTools):

    kunosTracks = {"ks_barcelona", "ks_black_cat_county", "ks_brands_hatch", "ks_drag", "ks_highlands", "ks_laguna_seca", "ks_monza66", "ks_nordschleife", "ks_nurburgring", "ks_red_bull_ring", "ks_silverstone", "ks_silverstone1967", "ks_vallelunga", "ks_zandvoort", "magione", "monza", "mugello", "spa", "trento-bondone", "drift", "imola"}

    def getUiJson(self, modPath):
        mod_ui_json = os.path.join(modPath, 'ui', 'ui_' + self.modType() + '.json')
        jsonFile = None
        if os.path.isfile(mod_ui_json):
            return common.parseJson(mod_ui_json)
        else:
            for layout in os.listdir(os.path.join(modPath, 'ui')):
                if os.path.isdir(os.path.join(modPath, 'ui',layout)):
                    mod_ui_json = os.path.join(modPath, 'ui', layout, 'ui_' + self.modType() + '.json')
                    if os.path.isfile(mod_ui_json):
                        return common.parseJson(mod_ui_json)

    def findModsWithTag(self, acdir, tagsToFind):
        foundTracks = []
        modspath = os.path.join(acdir, 'content', 'tracks')
        if not os.path.isdir(modspath):
            print("Error: Cannot find tracks dir " + modspath)
            return
        tracks = os.listdir(modspath)
        for track in tracks:
            modPath = os.path.join(modspath, track)
            mod_ui_json = os.path.join(modPath, 'ui', 'ui_' + self.modType() + '.json')
            if os.path.isfile(mod_ui_json):
                if self.tagsInJson(mod_ui_json, tagsToFind):
                    foundTracks.append(track)
            else:
                try:
                    for layout in os.listdir(os.path.join(modPath, 'ui')):
                        if os.path.isdir(os.path.join(modPath, 'ui',layout)):
                            mod_ui_json = os.path.join(modPath, 'ui', layout, 'ui_' + self.modType() + '.json')
                            if os.path.isfile(mod_ui_json):
                                if self.tagsInJson(mod_ui_json, tagsToFind):
                                    foundTracks.append(track)
                                    break
                except:
                    print("ERROR: invalid track " + track)
        return foundTracks





    def addCspTags(self, modId, acpath, modPath):
        tagsToAdd = []
        configFiles = [
            os.path.join(acpath, 'content',self.modType()  + 's', modId, 'extension', 'ext_config.ini'),
            os.path.join(acpath, 'extension','config', self.modType()  + 's', modId + '.ini'),
            os.path.join(acpath, 'extension', 'config', self.modType()  + 's', 'loaded', modId + '.ini')
        ]
        for configFile in configFiles:
            if os.path.isfile(configFile):
                config = common.readIniFile(configFile)
                if(config.has_section('GRASS_FX')):
                    tagsToAdd.append('grassfx')
                if(config.has_section('RAIN_FX')):
                    tagsToAdd.append('rainfx')
                if(config.has_section('LIGHT_SERIES_1')):
                    tagsToAdd.append('lightingfx')
                if(common.fileContainsWord(configFile, 'SEASON_WINTER')):
                    tagsToAdd.append('weatherfx')

        mod_ui_json = os.path.join(modPath, 'ui', 'ui_' + self.modType() + '.json')
        if os.path.isfile(mod_ui_json):
            self.updateTagsIfNecessary(mod_ui_json, tagsToAdd)
        else:
            for layout in os.listdir(os.path.join(modPath, 'ui')):
                if os.path.isdir(os.path.join(modPath, 'ui',layout)):
                    mod_ui_json = os.path.join(modPath, 'ui', layout, 'ui_' + self.modType() + '.json')
                    if os.path.isfile(mod_ui_json):
                        self.updateTagsIfNecessary(mod_ui_json, tagsToAdd)

    def updateTagsIfNecessary(self, mod_ui_json, tagsToAdd):
            jsonData = common.parseJson(mod_ui_json)
            newTags = list(set(jsonData['tags']) | set(tagsToAdd))
            if len(newTags) > len(jsonData['tags']):
                jsonData['tags'] = newTags
                with open(mod_ui_json, "w", encoding='utf-8') as jsonOutput:
                    json.dump(jsonData, jsonOutput, indent=2, ensure_ascii=False)
                print("updated tags for ui track " + mod_ui_json)    

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