import os
from configparser import ConfigParser

def isKunosDriver(fontName):
    return fontName in {"4c", "599_big", "599_mid","650S_big","650S_mid","a","aria",
    "arial","arial_big","audi_vln","aventador","aventador_b","aventador_mid","b","bosch",
    "c7_big","c7_mid","c7_new","comic","console","console_small","default","digital_big",
    "digital_big_f138","digital_big_italic","digital_mid","digital_toyota","digital_toyota_2",
    "e92_big","e92_mid","f312","gallardo_1","gallardo_2","german_led","german_led_mid",
    "ks_audi_r8_plus","ks_corvette_c7","ks_nissan_gtr","ks_ruf12r","led_audi","led_big",
    "led_med","mclarenmp4gt3","mercedes_sls","mg","Microgramma","Microsquare","mp4_big",
    "porsche_big","sls","ttcup","ttcup_big"}

def getFilesForDriver(acpath, fontname):
    driverFiles = []
    pngFileName = 'content' + os.sep + 'drivers3d' + os.sep + fontname + '.png' 
    txtFileName = 'content' + os.sep + 'fonts' + os.sep + fontname + '.txt' 
    if os.path.isfile(acpath + os.sep + pngFileName ):
        fontFiles.append(pngFileName)
    if os.path.isfile(acpath + os.sep + txtFileName ):
        fontFiles.append(txtFileName)
    print('found fonts ' + fontFiles.__str__ )
    return driverFiles
    
def find(acPath, carModId):
    config = ConfigParser()
    drivers3dPath = acPath + 'content' + os.sep + 'cars' + os.sep + carModId + os.sep + 'data' + os.sep + 'driver3d.ini'
    if os.path.isfile(drivers3dPath):
        config.read(drivers3dPath)
        section = "MODEL"
        if config.has_section(section):
            if config.has_option(section, 'NAME'):
                driverName = config.get(section, 'NAME')
                if not isKunosDriver(driverName):
                    return getFilesForDriver(acPath, driverName))
    return []