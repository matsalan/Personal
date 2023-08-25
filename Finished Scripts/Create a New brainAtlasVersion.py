import json

import os
import glob
import pprint
keywordList = []
#link the folder that has the atlas data
Jsonldfiles = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion\WHSSDatlas_v4.01'
brainAtlasVersion = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\brainAtlasVersion\WHSSDatlas_v4.01.jsonld'
#create a list that will be filled with all the parcellationEntity data
createList = []
#Go through all the files in the parcellationEntityVersion
for filename in glob.glob(os.path.join(Jsonldfiles, '*.jsonld')): #only process .JSON files in folder.      
    #open the files
    with open(filename, 'r') as file:
        
        # read the opened file in python dictionary format
        data = json.load(file)
        #if there is a filled list then append(put the name into) to the list
        if createList:
            dictentry = {"@id" : data["@id"]}
            createList.append(dictentry)
        #if not then start a new list which only happens once at the start
        else:
            dictentry = {"@id" : data["@id"]}
            createList = [dictentry]

#With the list done then open the brainAtlasVersion
with open(brainAtlasVersion, 'r', encoding="UTF-8") as brainAtlas:
    #Open in dictionary format
    brainAtLoaded = json.load(brainAtlas)
    #Fill in the list created 
    brainAtLoaded["hasTerminology"].update({"hasEntity" : createList})
    #save into the correct format
    newData = json.dumps(brainAtLoaded, indent=2)
    keepsamename = brainAtlasVersion.split('\\')

#Then open the new location in write mode so we can save it correctly
with open(brainAtlasVersion, 'w', newline = "\n", encoding="UTF-8") as file:

        # write
    file.write(newData)
    file.write("\n")

    