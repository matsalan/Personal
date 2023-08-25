import json
from tqdm import tqdm
import os
import glob
import pprint
import copy
import pandas as pd
from re import sub
def camel_case(s):
  s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])


#Define the origin folder of the pEV, i took a backup this can be the same as the save folder but risky because you overwrite the data
parcellationEntityVersion = r'C:\Users\mats_\Desktop\Ebrains\AllanBrain\AMBA_CCFv3-2015'
#Define where you want to save it
targetpath = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion\AMBA_CCFv3-2015'
#Where is the document with the codified hierarchy created by Excel reading program Allen
parentdoc = pd.read_excel(r"C:\Users\mats_\Desktop\Ebrains\Computer generated documents\Codified hierarchy 2015.xlsx")
#Where is the label file
labelfile = pd.read_csv(r'C:\Users\mats_\Desktop\Ebrains\AllanBrain\annotation_fixed.label', sep = "\t")
#which version are you using
version = "2015"


NoGoodDescription = []
#A for loop that goes through all the parcellationEntityVersions
for parcelEV in tqdm(glob.glob(os.path.join(parcellationEntityVersion, '*.jsonld'))): #only process .JSON files in folder. 
    #This opens the pEV
    with open(parcelEV, 'r') as parcelEnt:
        #This loads it into a dictionary format that can be modified
        OpenParcEnt = json.load(parcelEnt)
        #a copy used if there was no changes done
        Backup = copy.deepcopy(OpenParcEnt) 
        
        #This line finds the ID and finds the correct line in the hierarchy document
        findParent = parentdoc[parentdoc["ID"] == int(OpenParcEnt["hasAnnotation"][0]["internalIdentifier"])]

        
        #if bugged and the findParent could not be found then skip or you get an error
        if findParent.empty :
            continue
        
        #this for loop checks if there is actually a region called this in the label file to check for "fake" areas
        for lines in labelfile.iterrows():
            if lines[1][-1] == findParent["Name"].iloc[0]:
                break
            
        else:
            namedthing = findParent["Name"].iloc[0]
            namedID = findParent["ID"].iloc[0]
            namedParent = findParent["ParentName"].iloc[0]
                #If there is something wrong tell me
            
            NoGoodDescription.append(f"Did not find a matching line in the label {namedthing}, located at id : {namedID}, this is the parent : {namedParent}")
     
            
        #find the matching if you want to use it, however it has no current function
        findlabelmatch = labelfile[labelfile["LABEL"] == findParent["Name"].iloc[0]]
        
        #find the parent name
        parentactual = findParent["ParentName"].iloc[0]
        #remove commas for use in names
        if parentactual.find(",") >= 0:
            #Removed comma
            NameWithComma = parentactual
            parentactual = parentactual.replace(",", "")
        #append it to the json dictionary
        OpenParcEnt |= {"hasParent": [
    {
        "@id": f"https://openminds.ebrains.eu/instances/parcellationEntity/AMBA_CCFv3_{camel_case(parentactual)}"
    }
    ],}
        
        #heidi wanted the criteriatype gone so i set it to none, nvm disabeling sinc she wants it
        OpenParcEnt["hasAnnotation"][0]["criteriaQualityType"] = {
        "@id": "https://openminds.ebrains.eu/instances/criteriaQualityType/asserted"
      }
        if OpenParcEnt["name"].find("visual area") > 0:
            print(OpenParcEnt["name"])
            OpenParcEnt["hasAnnotation"][0]["criteriaQualityType"] = {
        "@id": "https://openminds.ebrains.eu/instances/criteriaQualityType/processive"
      } 
        
        #checking for version innovation if 2017 have new files
        shortlookup = OpenParcEnt["@id"].split("_")[-1]
        if version == "2017":
            #Edit the file to the file folder you want to compare and change the version number
            if os.path.isfile(f'C:\\Users\\mats_\\Desktop\\Ebrains\\Visual Code\\openMINDS_SANDS\\instances\\atlas\\parcellationEntityVersion\\AMBA_CCFv3-2015\\AMBA_CCFv3-2015_{shortlookup}.jsonld'):
                OpenParcEnt["versionInnovation"] = "unchanged"
            else:
                OpenParcEnt["versionInnovation"] = "new"
                
        
        #convert dictionary into jsonld format
        newData = json.dumps(OpenParcEnt, indent=2)
        
        #process the name to keep it the same
        keepsamename = parcelEV.split('\\')

        #save it, here i use newline and \n because it the rules (i think)
        with open(f"{targetpath}/{keepsamename[-1]}", 'w', newline="\n") as parcelEnt:
            parcelEnt.write(newData)
            parcelEnt.write("\n")

#Saves the error document with regions that are "fake"
with open(f'C:\\Users\\mats_\\Desktop\\Ebrains\\AllanBrain\\ErrorDocument {version}.txt', 'w') as f:
    for item in NoGoodDescription:
    # write each item on a new line
      f.write("%s\n" % item)
    print(f"ErrorDocument {version}.txt file is created from list of errors at 'C:\\Users\\mats_\\Desktop\\Ebrains\\AllanBrain\\ErrorDocument {version}.txt'", )


    