import json
from tqdm import tqdm
import os
import glob
import pprint
import copy
#Where are you parcellationEntities located, i suggest making a copy so you dont lose information
parcellationEntity = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\WHSSDatlas – Kopi'
#Where do you want to save them
targetpath = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntity\WHSSDatlas'
#Create a path for all the locations, i know a better way but i do not have time to implement it, you only need v1 and v401 if you want to update them
v101folder = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion\WHSSDatlas_v1.01'
v1folder = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion\WHSSDatlas_v1'
v2folder = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion\WHSSDatlas_v2'
v3folder = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion\WHSSDatlas_v3'
v301folder = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion\WHSSDatlas_v3.01'
v4folder = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion\WHSSDatlas_v4'
v401folder = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion\WHSSDatlas_v4.01'
#List for where we want to save them
hasVersionList = []
#Go through all the parcelationentities.
for parcelEntity in tqdm(glob.glob(os.path.join(parcellationEntity, '*.jsonld'))): #only process .JSON files in folder. 
    #open them and make a backup incase there should be no changes
    with open(parcelEntity, 'r') as parcelEnt:
        #Open in python dictionary form
        OpenParcEnt = json.load(parcelEnt)
        #not sure if you need a backup
        Backup = copy.deepcopy(OpenParcEnt)
    #Open all the files in the folders
    for v1fil in glob.glob(os.path.join(v1folder, '*.jsonld')): #only process .JSON files in folder. 
        #load
        with open(v1fil, 'r') as v1file:
            #make json into dictionary python format
            v1data = json.load(v1file)
            #check if the name matches and if it does than make the list longer
            if v1data["name"] == OpenParcEnt["name"]:
                hasVersionList.append({"@id" : v1data["@id"]})
    #append all the hasVersion that are already in the parcellationEntity onto the hasVersionList so they are kept
    if OpenParcEnt["hasVersion"]:
        for n in OpenParcEnt["hasVersion"]:
            hasVersionList.append(n)
    
                
    #do the same for next folder, this can be copied for every version you want to check for    
    for v401fil in glob.glob(os.path.join(v401folder, '*.jsonld')): #only process .JSON files in folder. 
        
        with open(v401fil, 'r') as v401file:

            v401data = json.load(v401file)
            if v401data["name"] == OpenParcEnt["name"]:
                hasVersionList.append({"@id" : v401data["@id"]})
    

    #insert the version list into the temporary dictionary 
    OpenParcEnt.update({"hasVersion" : hasVersionList})
    #Save it in json format
    newData = json.dumps(OpenParcEnt, indent=2)
    #empty the list for next round
    hasVersionList = []
    #save it
    keepsamename = parcelEntity.split('\\')
    #if there is a list then save it
    if len(OpenParcEnt["hasVersion"]) > 0:
        with open(f"{targetpath}/{keepsamename[-1]}", 'w', newline = "\n") as parcelEnt:
            parcelEnt.write(newData)
            parcelEnt.write("\n")
    #if no list then dont make any changes and save it, this also updates the format to the correct one
    else: 
        newone = json.dumps(Backup, indent=2)
        with open(f"{targetpath}/{keepsamename[-1]}", 'w', newline ="\n") as parcelEnt:
            parcelEnt.write(newone)
            parcelEnt.write("\n")
            

    