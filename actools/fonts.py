import os
from actools import common
from configparser import ConfigParser

def isKunosFont(fontName):
    return fontName in {"4c", "599_big", "599_mid","650S_big","650S_mid","a","aria",
    "arial","arial_big","audi_vln","aventador","aventador_b","aventador_mid","b","bosch",
    "c7_big","c7_mid","c7_new","comic","console","console_small","default","digital_big",
    "digital_big_f138","digital_big_italic","digital_mid","digital_toyota","digital_toyota_2",
    "e92_big","e92_mid","f312","gallardo_1","gallardo_2","german_led","german_led_mid",
    "ks_audi_r8_plus","ks_corvette_c7","ks_nissan_gtr","ks_ruf12r","led_audi","led_big",
    "led_med","mclarenmp4gt3","mercedes_sls","mg","Microgramma","Microsquare","mp4_big",
    "porsche_big","sls","ttcup","ttcup_big"}

def getFilesForFont(acpath, fontname):
    fontFiles = []
    pngFileName = 'content' + os.sep + 'fonts' + os.sep + fontname + '.png' 
    txtFileName = 'content' + os.sep + 'fonts' + os.sep + fontname + '.txt' 
    ttfFileName = 'content' + os.sep + 'fonts' + os.sep + fontname + '.ttf' 
    if os.path.isfile(acpath + os.sep + pngFileName ):
        fontFiles.append(pngFileName)
        print("\tfound font file " + pngFileName)
    if os.path.isfile(acpath + os.sep + txtFileName ):
        fontFiles.append(txtFileName)
        print("\tfound font file " + txtFileName)
    if os.path.isfile(acpath + os.sep + ttfFileName ):
        fontFiles.append(ttfFileName)
        print("\tfound font file " + ttfFileName)
    return fontFiles

def findFontsInDigitalInstruments(acPath, digitalInstrumentsPath, fontsFound, fontFiles):
    if os.path.isfile(digitalInstrumentsPath):
        config = common.readIniFile(digitalInstrumentsPath)
        i = 0
        section = "ITEM_" + str(i)
        while config.has_section(section):
            if config.has_option(section, 'FONT'):
                fontName = config.get(section, 'FONT')
                if not isKunosFont(fontName) and not fontName in fontsFound:
                    fontFiles.extend(getFilesForFont(acPath, fontName))
                    fontsFound.add(fontName)
            i = i + 1
            section = "ITEM_" + str(i)

def find(acPath, carModId, dataAcdWorkdir):
    fontsFound = set() 
    fontFiles = []
    digitalInstrumentsPath = acPath + os.sep  + 'content' + os.sep + 'cars' + os.sep + carModId + os.sep + 'data' + os.sep + 'digital_instruments.ini'
    findFontsInDigitalInstruments(acPath, digitalInstrumentsPath, fontsFound, fontFiles)
    if not dataAcdWorkdir == None:
        digitalInstrumentsAcdPath = os.path.join(dataAcdWorkdir, 'digital_instruments.ini')
        if os.path.isfile(digitalInstrumentsAcdPath):
            findFontsInDigitalInstruments(acPath, digitalInstrumentsAcdPath, fontsFound, fontFiles)
    return fontFiles
