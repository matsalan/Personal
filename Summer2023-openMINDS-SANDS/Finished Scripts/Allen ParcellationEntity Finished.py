import json
from tqdm import tqdm
import os
import glob
import pprint
import pandas as pd
from re import sub
#Defined  where parcellation Entities shall be located
parcellationEntity = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntity\AMBA_CCFv3'
#Where is the different versions located
v2015folder = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion\AMBA_CCFv3-2015'
v2017folder = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion\AMBA_CCFv3-2017'

#Read the hierarchy produced by the excel reading programs, remember you need to create the 
parent2015 = pd.read_excel(r"C:\Users\mats_\Desktop\Ebrains\Computer generated documents\Codified hierarchy 2015.xlsx")
parent2017 = pd.read_excel(r"C:\Users\mats_\Desktop\Ebrains\Computer generated documents\Codified hierarchy 2017.xlsx")
def camel_case(s):
  s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])

#Making a list that can be filled with the versions
hasVersionList = []

#glob outside once because slow process, this creates a list of all the jsonLds
globbing = glob.glob(os.path.join(v2015folder, '*.jsonld'))
#go through all the json files
for v1fil in globbing: #only process .JSON files in folder. 
    #Open the files
    with open(v1fil, 'r') as v1file:
        #load the files
        v1data = json.load(v1file)

        #extract name and the lookup label for use
        shortlookup = v1data["@id"].split("_")[-1]
        lookupLabel = f"AMBA_CCFv3_{shortlookup}"
        actualname = v1data["name"]
        #Insert into standard format
        standardformat = {
    "@context": {
        "@vocab": "https://openminds.ebrains.eu/vocab/"
    },
    "@id": f"https://openminds.ebrains.eu/instances/parcellationEntity/AMBA_CCFv3_{shortlookup}",
    "@type": "https://openminds.ebrains.eu/sands/ParcellationEntity",
    "abbreviation": None,
    "alternateName": None,
    "definition": None,
    "hasParent": None,
    "hasVersion": [{
        "@id" : f"{v1data['@id']}"
        }],
    "lookupLabel": f"{lookupLabel}",
    "name": f"{actualname}",
    "ontologyIdentifier": None,
    "relatedUBERONTerm": None
    }

        #Find the matching parent to the ID of the current file
        matchingParentRow = parent2015[parent2015["id"] == int(v1data["hasAnnotation"][0]["internalIdentifier"])]
        #If there is not match then it is empty so ignore it
        if matchingParentRow.empty:
            continue
        else:
            #Process the name to remove commas, should perhaps be expanded to other symbols
            if v1data["name"].find(",") >= 0:
                #Removed comma
                NameWithComma = matchingParentRow["parent"].iloc[0]
                Name = camel_case(matchingParentRow["parent"].iloc[0].replace(",", ""))
            else: 
                Name = camel_case(matchingParentRow["parent"].iloc[0])
                #insert into the format
            standardformat |= {"hasParent" : [{
                "@id" : f"https://openminds.ebrains.eu/instances/parcellationEntity/AMBA_CCFv3_{Name}"
            }]}
            
        #save the file
        with open(f'{parcellationEntity}\\AMBA_CCFv3_{shortlookup}.jsonld', 'w', newline ="\n") as parcelEnt:
            stand = json.dumps(standardformat, indent=2)
            parcelEnt.write(stand)
            parcelEnt.write("\n")
#Make a list of all the jsonlds       
globbing2 = glob.glob(os.path.join(v2017folder, '*.jsonld'))
#Go through all the parcellationEntityVersions 
for v101fil in globbing2: #only process .JSON files in folder. 
    
    #Open them
    with open(v101fil, 'r') as v101file:
        #Load them into python format
        v101data = json.load(v101file)
        #Extract important data that we use later for the standard format
        shortlookup = v101data["@id"].split("_")[-1]
        lookupLabel = f"AMBA_CCFv3_{shortlookup}"
        actualname = v101data["name"]
        
        #Check if there is a parcellationEntitiy already for the pEV
        if os.path.isfile(f'C:\\Users\\mats_\\Desktop\\Ebrains\\Visual Code\\openMINDS_SANDS\\instances\\atlas\\parcellationEntity\\AMBA_CCFv3\\AMBA_CCFv3_{shortlookup}.jsonld'):
            #If found then open the pE
            with open(f'C:\\Users\\mats_\\Desktop\\Ebrains\\Visual Code\\openMINDS_SANDS\\instances\\atlas\\parcellationEntity\\AMBA_CCFv3\\AMBA_CCFv3_{shortlookup}.jsonld', 'r') as parcelEnt:
        
                parcelEntdata = json.load(parcelEnt)
                #Check if there is any changes in the name 
                if parcelEntdata["lookupLabel"] != lookupLabel:
                    print("siifra ", lookupLabel )
                if parcelEntdata["name"] != actualname:
                    print("ikke matchende navn ", actualname)
                #extract the versionlist
                has2015 = parcelEntdata["hasVersion"][0]
                
                #insert both the 2015 and the new version name into a list
                hasVersionList.append(has2015)
                hasVersionList.append({"@id" : v101data["@id"]})
                
                #Insert the list onto the standardformat
                parcelEntdata["hasVersion"] = hasVersionList
                #save into json format
                stand = json.dumps(parcelEntdata, indent=2)
                #save it to file
                with open(f'{parcellationEntity}\\AMBA_CCFv3_{shortlookup}.jsonld', 'w', newline ="\n") as parcelEnt:
                    
                    parcelEnt.write(stand)
                    parcelEnt.write("\n")
                #does not include has parent changes
        #If there was no file for the name then create a new one
        else: 
            #standard format of the parcellationEntity
            standardformat = {
        "@context": {
            "@vocab": "https://openminds.ebrains.eu/vocab/"
        },
        "@id": f"https://openminds.ebrains.eu/instances/parcellationEntity/AMBA_CCFv3_{shortlookup}",
        "@type": "https://openminds.ebrains.eu/sands/ParcellationEntity",
        "abbreviation": None,
        "alternateName": None,
        "definition": None,
        "hasParent": None,
        "hasVersion": [{
            "@id" : f"{v101data['@id']}"
            }],
        "lookupLabel": f"{lookupLabel}",
        "name": f"{actualname}",
        "ontologyIdentifier": None,
        "relatedUBERONTerm": None
        }
            #Find the matching parent to the id of the current file, see above description as this is the exact same
            matchingParentRow = parent2017[parent2017["id"] == int(v1data["hasAnnotation"][0]["internalIdentifier"])]
            if matchingParentRow.empty:
                continue
            else:
                if v101data["parent"].find(",") >= 0:
                    #Removed comma
                    NameWithComma = matchingParentRow["parent"].iloc[0]
                    Name = camel_case(matchingParentRow["parent"].iloc[0].replace(",", ""))
                else: 
                    Name = camel_case(matchingParentRow["parent"].iloc[0])
                standardformat |= {"hasParent" : [{
                    "@id" : f"https://openminds.ebrains.eu/instances/parcellationEntity/AMBA_CCFv3_{Name}"
                }]}
                
            with open(f'{parcellationEntity}\\AMBA_CCFv3_{shortlookup}.jsonld', 'w', newline ="\n") as parcelEnt:
                stand = json.dumps(standardformat, indent=2)
                parcelEnt.write(stand)
                parcelEnt.write("\n")
                    
        hasVersionList = []
        
        
        

        
            

    