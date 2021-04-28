import tempfile
import os
from actools import common
from actools import mods
from actools import fonts
from actools import drivers
import json
import urllib.parse

class CarTools(mods.ModTools):
    kunosCars = {
            "abarth500",
            "abarth500_s1",
            "alfa_romeo_giulietta_qv",
            "alfa_romeo_giulietta_qv_le",
            "bmw_1m",
            "bmw_1m_s3",
            "bmw_m3_e30",
            "bmw_m3_e30_drift",
            "bmw_m3_e30_dtm",
            "bmw_m3_e30_gra",
            "bmw_m3_e30_s1",
            "bmw_m3_e92",
            "bmw_m3_e92_drift",
            "bmw_m3_e92_s1",
            "bmw_m3_gt2",
            "bmw_z4",
            "bmw_z4_drift",
            "bmw_z4_gt3",
            "bmw_z4_s1",
            "ferrari_312t",
            "ferrari_458",
            "ferrari_458_gt2",
            "ferrari_458_s3",
            "ferrari_599xxevo",
            "ferrari_f40",
            "ferrari_f40_s3",
            "ferrari_laferrari",
            "ks_abarth500_assetto_corse",
            "ks_abarth_595ss",
            "ks_abarth_595ss_s1",
            "ks_abarth_595ss_s2",
            "ks_alfa_33_stradale",
            "ks_alfa_giulia_qv",
            "ks_alfa_mito_qv",
            "ks_alfa_romeo_155_v6",
            "ks_alfa_romeo_4c",
            "ks_alfa_romeo_gta",
            "ks_audi_a1s1",
            "ks_audi_r18_etron_quattro",
            "ks_audi_r8_lms",
            "ks_audi_r8_lms_2016",
            "ks_audi_r8_plus",
            "ks_audi_sport_quattro",
            "ks_audi_sport_quattro_rally",
            "ks_audi_sport_quattro_s1",
            "ks_audi_tt_cup",
            "ks_audi_tt_vln",
            "ks_bmw_m235i_racing",
            "ks_bmw_m4",
            "ks_bmw_m4_akrapovic",
            "ks_corvette_c7_stingray",
            "ks_corvette_c7r",
            "ks_ferrari_250_gto",
            "ks_ferrari_288_gto",
            "ks_ferrari_312_67",
            "ks_ferrari_330_p4",
            "ks_ferrari_488_gt3",
            "ks_ferrari_488_gtb",
            "ks_ferrari_812_superfast",
            "ks_ferrari_f138",
            "ks_ferrari_f2004",
            "ks_ferrari_fxx_k",
            "ks_ferrari_sf15t",
            "ks_ferrari_sf70h",
            "ks_ford_escort_mk1",
            "ks_ford_gt40",
            "ks_ford_mustang_2015",
            "ks_glickenhaus_scg003",
            "ks_lamborghini_aventador_sv",
            "ks_lamborghini_countach",
            "ks_lamborghini_countach_s1",
            "ks_lamborghini_gallardo_sl",
            "ks_lamborghini_gallardo_sl_s3",
            "ks_lamborghini_huracan_gt3",
            "ks_lamborghini_huracan_performante",
            "ks_lamborghini_huracan_st",
            "ks_lamborghini_miura_sv",
            "ks_lamborghini_sesto_elemento",
            "ks_lotus_25",
            "ks_lotus_3_eleven",
            "ks_lotus_72d",
            "ks_maserati_250f_12cyl",
            "ks_maserati_250f_6cyl",
            "ks_maserati_alfieri",
            "ks_maserati_gt_mc_gt4",
            "ks_maserati_levante",
            "ks_maserati_mc12_gt1",
            "ks_maserati_quattroporte",
            "ks_mazda_787b",
            "ks_mazda_miata",
            "ks_mazda_mx5_cup",
            "ks_mazda_mx5_nd",
            "ks_mazda_rx7_spirit_r",
            "ks_mazda_rx7_tuned",
            "ks_mclaren_570s",
            "ks_mclaren_650_gt3",
            "ks_mclaren_f1_gtr",
            "ks_mclaren_p1",
            "ks_mclaren_p1_gtr",
            "ks_mercedes_190_evo2",
            "ks_mercedes_amg_gt3",
            "ks_mercedes_c9",
            "ks_nissan_370z",
            "ks_nissan_gtr",
            "ks_nissan_gtr_gt3",
            "ks_nissan_skyline_r34",
            "ks_pagani_huayra_bc",
            "ks_porsche_718_boxster_s",
            "ks_porsche_718_boxster_s_pdk",
            "ks_porsche_718_cayman_s",
            "ks_porsche_718_spyder_rs",
            "ks_porsche_908_lh",
            "ks_porsche_911_carrera_rsr",
            "ks_porsche_911_gt1",
            "ks_porsche_911_gt3_cup_2017",
            "ks_porsche_911_gt3_r_2016",
            "ks_porsche_911_gt3_rs",
            "ks_porsche_911_r",
            "ks_porsche_911_rsr_2017",
            "ks_porsche_917_30",
            "ks_porsche_917_k",
            "ks_porsche_918_spyder",
            "ks_porsche_919_hybrid_2015",
            "ks_porsche_919_hybrid_2016",
            "ks_porsche_935_78_moby_dick",
            "ks_porsche_962c_longtail",
            "ks_porsche_962c_shorttail",
            "ks_porsche_991_carrera_s",
            "ks_porsche_991_turbo_s",
            "ks_porsche_cayenne",
            "ks_porsche_cayman_gt4_clubsport",
            "ks_porsche_cayman_gt4_std",
            "ks_porsche_macan",
            "ks_porsche_panamera",
            "ks_praga_r1",
            "ks_ruf_rt12r",
            "ks_ruf_rt12r_awd",
            "ks_toyota_ae86",
            "ks_toyota_ae86_drift",
            "ks_toyota_ae86_tuned",
            "ks_toyota_celica_st185",
            "ks_toyota_gt86",
            "ks_toyota_supra_mkiv",
            "ks_toyota_supra_mkiv_drift",
            "ks_toyota_supra_mkiv_tuned",
            "ks_toyota_ts040",
            "ktm_xbow_r",
            "lotus_2_eleven",
            "lotus_2_eleven_gt4",
            "lotus_49",
            "lotus_98t",
            "lotus_elise_sc",
            "lotus_elise_sc_s1",
            "lotus_elise_sc_s2",
            "lotus_evora_gtc",
            "lotus_evora_gte",
            "lotus_evora_gte_carbon",
            "lotus_evora_gx",
            "lotus_evora_s",
            "lotus_evora_s_s2",
            "lotus_exige_240",
            "lotus_exige_240_s3",
            "lotus_exige_s",
            "lotus_exige_s_roadster",
            "lotus_exige_scura",
            "lotus_exige_v6_cup",
            "lotus_exos_125",
            "lotus_exos_125_s1",
            "mclaren_mp412c",
            "mclaren_mp412c_gt3",
            "mercedes_sls",
            "mercedes_sls_gt3",
            "p4-5_2011",
            "pagani_huayra",
            "pagani_zonda_r",
            "ruf_yellowbird",
            "shelby_cobra_427sc",
            "tatuusfa1"
            }
    def updateModUrlForAcServer(self, modDir, archiveName, urlPrefix, dir ):
        metadataFilePath =  os.path.join(modDir, "ui", "ui_car.json")
        jsonData = common.parseJson(metadataFilePath)
        jsonData["downloadURL"] = urlPrefix + urllib.parse.quote(archiveName) + '.7z'
        with open(metadataFilePath, "w") as jsonFile:
            json.dump(jsonData, jsonFile, indent=2)

    def getUiJson(self, modPath):
        mod_ui_json = os.path.join(modPath, 'ui', 'ui_' + self.modType() + '.json')
        return common.parseJson(mod_ui_json)

    def modType(self): 
        return "car"

    def isKunosMod(self, modId):
        return modId in self.kunosCars
        
    
    def destination(self, params):
        return params.carsDestination

    def modDownloadUrlPrefix(self, params):
        return params.carDownloadUrlPrefix

    def findModsWithTag(self, acdir, tagsToFind):
        foundCars = []
        modspath = os.path.join(acdir, 'content', 'cars')
        if not os.path.isdir(modspath):
            print("Error: Cannot find cars dir " + modspath)
            return
        cars = os.listdir(modspath)
        for car in cars:
            modPath = os.path.join(modspath, car)
            mod_ui_json = os.path.join(modPath, 'ui', 'ui_' + self.modType() + '.json')
            if os.path.isfile(mod_ui_json):
                if self.tagsInJson(mod_ui_json, tagsToFind):
                    foundCars.append(car)
        return foundCars

    def modFiles(self, modId, acpath):
        filesArray = [
        # mod main folder
        os.path.join('content',self.modType() + 's', modId),
        # extension config file
         os.path.join('extension', 'config', self.modType()  + 's', modId + '.ini'),
        # extension config file
         os.path.join('extension', 'config', self.modType()  + 's', 'loaded', modId + '.ini'),
         os.path.join('extension', 'config', self.modType()  + 's', modId + '.ini.blm')
        ]

        dataAcdFile = os.path.join(acpath, 'content', 'cars', modId, 'data.acd')
        if os.path.isfile(dataAcdFile):
            dataAcdWorkdir = tempfile.mkdtemp()
            common.extractAcd(self.quickbmsexec, dataAcdFile, dataAcdWorkdir)
            filesArray.extend(fonts.find(acpath, modId, dataAcdWorkdir))
            filesArray.extend(drivers.find(acpath, modId, dataAcdWorkdir))
        return filesArray