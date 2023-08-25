import json

import os
import glob
import pprint
keywordList = []

#find the correct path
path = '../../JsonId that needs adjustments'
#make alist with all the json files that need adjustment
globoutside = glob.glob(os.path.join(path, '*.jsonld'))
#go through all the files
for filename in globoutside: #only process .JSON files in folder.      
    #open file
    with open(filename, 'r') as file:

        # read it in correct python format aka dictionary
        data = json.load(file)
        
        # extract information from the pEV
        id = data["@id"] 
        alternativeName = data["alternativeName"]
        lookupLabel = data["lookupLabel"]
        name = data["name"]
        versionIdentifier = data["versionIdentifier"]

        #New dictionary form at and insert the information in the correct alphabetical order
        NewJsonId = {
        "@context": {
            "@vocab": "https://openminds.ebrains.eu/vocab/"
        },
        "@id": id,
        "@type": "https://openminds.ebrains.eu/sands/ParcellationEntityVersion",
        "additionalRemarks": None,
        "alternativeName": alternativeName,
        "correctedName": None,
        "hasAnnotation": [
            {
                "@type": "https://openminds.ebrains.eu/sands/AtlasAnnotation",
                "bestViewPoint": None,
                "criteria": None,
                "criteriaQualityType": None,
                "displayColor": None,
                "inspiredBy": None,
                "internalIdentifier": None,
                "laterality": [
                    {
                        "@id": "https://openminds.ebrains.eu/instances/laterality/left"
                    },
                    {
                        "@id": "https://openminds.ebrains.eu/instances/laterality/right"
                    }
                ],
                "visualizedIn": None
            }
        ],
        "hasParent": None,
        "lookupLabel": lookupLabel,
        "name": name,
        "ontologyIdentifier": None,
        "relationAssessment": None,
        "versionIdentifier": versionIdentifier,
        "versionInnovation": None,

    }
        #dump data from dictionary format to json format
        newData = json.dumps(NewJsonId, indent=2)
        #splti to keep the same name
        keepsamename = filename.split('\\')
    # save it in the location that is given here
    with open(f'C:\\Users\\mats_\\OneDrive\\Dokumenter fra laptop\\Dokumenter\\GitHub\\openMINDS_SANDS\\instances\\atlas\\parcellationEntityVersion\\RBSC_PW_v6\\{keepsamename[1]}', 'w', newline = "\n") as file:
        
        # write
        file.write(newData)
        file.write('\n')
    
    