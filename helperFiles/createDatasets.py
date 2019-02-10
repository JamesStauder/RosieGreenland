import time
from classes.Dataset import *

'''
Function: createInitialDataSets
Argument list: 
Purpose: Create dictionary of datasets
Return types, values:
Dependencies:  h5py, Dataset Class
Creator: James Stauder
Date created: 1/31/18
Last edited: 1/31/18
'''


def createInitialDatasets():
    print "Creating data sets"
    t0 = time.time()

    datasetDict = {}

    dataFile = h5py.File(dataFileName, 'r')

    x = dataFile['Grid']['x500'][:]
    y = dataFile['Grid']['y500'][:]

    map['x'] = x
    map['y'] = y

    velocityData = np.sqrt(dataFile['Velocity']['VX500'][:]**2 + dataFile['Velocity']['VY500'][:]**2)
    datasetDict['velocity'] = Dataset('velocity', velocityData)

    smbData = dataFile['Smb_T2m']['smb500'][:]
    datasetDict['smb'] = Dataset('smb', smbData)

    bedData = dataFile['BedMachine']['bed500'][:]
    datasetDict['bed'] = Dataset('bed', bedData)

    surfaceData = dataFile['BedMachine']['surface500'][:]
    datasetDict['surface'] = Dataset('surface', surfaceData)

    thicknessData = dataFile['BedMachine']['thickness500'][:]
    datasetDict['thickness'] = Dataset('thickness', thicknessData)

    t2mData = dataFile['Smb_T2m']['t2m500'][:]
    datasetDict['t2m'] = Dataset('t2m', t2mData)


    dataFile.close()







    print "Loaded all data sets in ", time.time() - t0, " seconds"
    return datasetDict
