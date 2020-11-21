import os
import tempfile
from actools import common

def transformToValidMod(params, archiveSrcPath):
    if not os.path.isfile(archiveSrcPath ):
        print("Cannot find archive " + archiveSrcPath)
        return

    workdir = tempfile.mkdtemp()
    common.unzipFileToDir(params.sevenzipexec, archiveSrcPath, workdir)

    