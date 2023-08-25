import json

import os
import glob
import pprint
keywordList = []
Jsonldfiles = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion\AMBA_CCFv3-2017'
brainAtlasVersion = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\brainAtlasVersion\AMBA_CCFv3-2017.jsonld'
createList = []
for filename in glob.glob(os.path.join(Jsonldfiles, '*.jsonld')): #only process .JSON files in folder.      
    
    with open(filename, 'r') as file:
        
        # read
        data = json.load(file)
        
        if createList:
            dictentry = {"@id" : data["@id"]}
            createList.append(dictentry)

        else:
            dictentry = {"@id" : data["@id"]}
            createList = [dictentry]
        
with open(brainAtlasVersion, 'r', encoding="UTF-8") as brainAtlas:
    brainAtLoaded = json.load(brainAtlas)
    brainAtLoaded["hasTerminology"].update({"hasEntity" : createList})

    newData = json.dumps(brainAtLoaded, indent=2)
    keepsamename = brainAtlasVersion.split('\\')
    print(newData)
    #open
with open(brainAtlasVersion, 'w', newline = "\n", encoding="UTF-8") as file:

        # write
    file.write(newData)
    file.write("\n")

    