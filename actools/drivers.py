import os
from actools import common

def isKunosDriver(fontName):
    return fontName in {"2016_Driver","driver","driver_60","driver_70","driver_80","driver_back","driver_lod_b","driver_no_HANS","driver_ocolus",
    "new_driver"}

def isKunosCrew(crewName, crewType):
    if crewType == 'SUIT':
        return crewName.startswith("\\type1\\") or crewName.startswith("\\type2\\")
    elif crewType == 'HELMET':
        return crewName in {"\\beige","\\black","\\blue","\\brown","\\cyan","\\green","\\grey","\\orange","\\purple","\\red","\\white","\\yellow"}
    elif crewType == 'BRAND':
        return crewName in {"\\abarth", "\\abarth2", "\\alfa", "\\alfa2", "\\audi", "\\audi2", "\\bmw", "\\chevy", "\\chevy2", "\\cobra", "\\cobra2", "\\ferrari", "\\ferrari2", "\\ford", "\\ktm",
         "\\lamborghini", "\\lamborghini2", "\\lotus", 
        "\\lotus_classic", "\\maserati", "\\maserati2", "\\mazda", "\\mazda2", "\\mclaren", "\\mclaren2", "\\mercedes", "\\mercedes2", "\\nissan", "\\nissan2", "\\pagani", 
        "\\porsche", "\\porsche2", "\\praga", "\\praga2", "\\PSD", "\\ruf", 
        "\\ruf2", "\\scg", "\\tatuus", "\\toyota", "\\toyota2"}

def getFilesForDriver(acpath, drivername):
    driverFiles = []
    kn5filename = 'content' + os.sep + 'driver' + os.sep + drivername + '.kn5' 
    if os.path.isfile(acpath + os.sep + kn5filename ):
        driverFiles.append(kn5filename)
    print('found driver file ' + kn5filename + " for driver " + drivername)
    return driverFiles


def getFilesForCrew(acPath, crewType, crewName):
    crewFiles = []
    crewDir = 'content' + os.sep + 'texture' + os.sep + 'crew_' + crewType.lower() + crewName + os.sep
    if os.path.isdir(acPath + os.sep + crewDir):
        crewFiles.append(crewDir )
    print('found crew dir ' + crewDir )
    return crewFiles

def findDriverInSection(config, section, driversFiles, acPath, driversFound):
    if config.has_section(section):
                if config.has_option(section, 'NAME'):
                    driverName = config.get(section, 'NAME')
                    if not isKunosDriver(driverName) and not driverName in driversFound:
                        print("found driver " + driverName)
                        driversFound.add(driverName)
                        driversFiles.extend(getFilesForDriver(acPath, driverName))

def findCrewFiles(skinPath, crewType, driversFiles, acPath, crewsFound):
    skinConfig = skinPath + os.sep + 'skin.ini'
    if os.path.isfile(skinConfig):
        config = common.readIniFile(skinConfig)
        section = 'CREW'
        if config.has_section(section):
                    if config.has_option(section, crewType):
                        crewName = config.get(section, crewType)
                        if not isKunosCrew(crewName, crewType) and not crewName in crewsFound:
                            crewsFound.add(crewName)
                            driversFiles.extend(getFilesForCrew(acPath, crewType, crewName))

def find(acPath, carModId):
    driversFiles = []
    driversFound = set() 
    helmetsFound = set() 
    suitsFound = set() 
    brandFound = set() 
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
                findCrewFiles(skinPath, 'SUIT', driversFiles, acPath, suitsFound)
                findCrewFiles(skinPath, 'HELMET', driversFiles, acPath, helmetsFound)
                findCrewFiles(skinPath, 'BRAND', driversFiles, acPath, brandFound)
    return driversFiles