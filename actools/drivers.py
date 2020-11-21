import os
from actools import common

def isKunosDriver(fontName):
    return fontName in {"2016_Driver","driver","driver_60","driver_70","driver_80","driver_back","driver_lod_b","driver_no_HANS","driver_ocolus",
    "new_driver"}

def getFilesForDriver(acpath, drivername):
    driverFiles = []
    kn5filename = 'content' + os.sep + 'driver' + os.sep + drivername + '.kn5' 
    if os.path.isfile(acpath + os.sep + kn5filename ):
        driverFiles.append(kn5filename)
    print('found driver file ' + kn5filename + " for driver " + drivername)
    return driverFiles


def findDriverInSection(config, section, driversFiles, acPath, driversFound):
    if config.has_section(section):
                if config.has_option(section, 'NAME'):
                    driverName = config.get(section, 'NAME')
                    if not isKunosDriver(driverName) and not driverName in driversFound:
                        print("found driver " + driverName)
                        driversFound.add(driverName)
                        driversFiles.extend(getFilesForDriver(acPath, driverName))

def find(acPath, carModId):
    driversFiles = []
    driversFound = set() 
    drivers3dPath = acPath + os.sep + 'content' + os.sep + 'cars' + os.sep + carModId + os.sep + 'data' + os.sep + 'driver3d.ini'
    if os.path.isfile(drivers3dPath):
        config = common.readIniFile(drivers3dPath)
        findDriverInSection(config, "MODEL", driversFiles, acPath, driversFound)
    skinsPath = acPath + os.sep + 'content' + os.sep + 'cars' + os.sep + carModId + os.sep + 'skins'
    if os.path.isdir(skinsPath):
        for skin in os.listdir(skinsPath):
            skinPath = skinsPath + os.sep + skin
            if os.path.isdir(skinPath):
                extConfig = skinPath + os.sep + 'ext_config.ini'
                if os.path.isfile(extConfig):
                    config = common.readIniFile(extConfig)
                    findDriverInSection(config, "DRIVER3D_MODEL", driversFiles, acPath, driversFound)
    return driversFiles