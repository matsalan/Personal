import json
from tqdm import tqdm
import os
import glob
import pprint
import copy
#Importing the required packages
import json
import os
import re
import pandas as pd
from re import sub
from lxml import etree
from bs4 import BeautifulSoup
import numpy as np
import warnings as wn
import math

def camel_case(s):
  s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])


def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""
keywordList = []
#I have a copy of the parcellation Entityversions so i have blue print that does not change in case i want to make changes in the code
parcellationEntityVersion = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\parcellationEntityVersion'

InspiredByLink = "https://www.nitrc.org/frs/?group_id=1081"
#Target destionation for the parcellationEntityVersions should be in the openMINDS SANDS path 
destination = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion'
#Write the versions you want to update
versions = ["v1.01", "v2", "v3", "v3.01", "v4"]
xmlpath = f"C:\\Users\\mats_\\Desktop\\Ebrains\\"  
#A oop that iterates through each of the different version folders 
for vers in tqdm(versions):
    #Since the destionation and origin changes based on which loop iteration you are on i need to do a deep copy that cuts the connection between the variable and the new variable
    originfolder = copy.deepcopy(f"{parcellationEntityVersion}\WHSSDatlas_{vers}")
    globoutside = glob.glob(os.path.join(originfolder, '*.jsonld'))
    #open the ilf files
    ilfopen = copy.deepcopy(f"{xmlpath}\\WHS {vers}\\WHS_SD_rat_atlas_{vers}_labels.ilf")
    #As ilf files are an xml file i parse them with etree converting it to a form python can work with
    root=etree.parse((ilfopen))
    #Convert the parsed xml file into a string, which makes the file format way easier to work with.
    xmlString = etree.tostring(root)
    #Convert it into beautiful soup because it is a wonderful tool.
    soup = BeautifulSoup(xmlString)
    #A loop that goes throuh all the files in the folder in focus 
    for datafile in globoutside:
        #This line opens the file so that python can read it
        with open(datafile, 'r') as parcelEntVer:
            #This converts the json data into a dictionary entry
            OpenParcEnt = json.load(parcelEntVer)
            
            #Extract the ID for comparisons between VersionInnovation and Anchorpoint data
            Id = OpenParcEnt["hasAnnotation"][0]["internalIdentifier"]

            OpenParcEnt["hasAnnotation"][0].update({"inspiredBy" :[
                {
                    "@id" : InspiredByLink
                }
            ]})
            #After version three there was abbreviations but not prior according to the ilf files there was only full names put in as abbraviation
            if vers != "v1" and vers != "v1.01" and vers != "v2":
                #Extract abbraviation from the first entry in alternateName list
                abbre = OpenParcEnt["alternateName"][0]
                #Append to the files copy the abbreviation
                OpenParcEnt |= {"abbreviation" : abbre}
            
            
            FoundParent = str(soup.find(id=int(Id)).find_parent()).split('<')[1].split('>')[0]
            if not FoundParent == "structure":
                ParentRegion = FoundParent.split('name="')[1].split('"')[0]
                if ParentRegion.find(",") >= 0:
                    ParentRegion = ParentRegion.replace(",","")
                if ParentRegion.find("(") >= 0:
                    ParentRegion = ParentRegion.replace("(","")
                if ParentRegion.find(")") >= 0:
                    ParentRegion = ParentRegion.replace(")","")
                if ParentRegion.find("-") >= 0:
                    ParentRegion = ParentRegion.replace("-","")

                ParentRegion = camel_case(ParentRegion)
                    
                OpenParcEnt.update({"hasParent" : [{
                    "@id": f"https://openminds.ebrains.eu/instances/parcellationEntity/WHSSDatlas_{ParentRegion}" 
                }]})   
            
            
            
            
            
            
            
            #Write the pathway for the version innovation document
            VerInnoFile = pd.read_excel(r"C:\Users\mats_\Desktop\Ebrains\WHS all versions\WHS_SD_rat_brain_atlas_v4_Pythonmodified.xlsx")
            #Write the versions included in the version innovation document
            Versions = ["v1", "v1.01", "v2", "v3", "v3.01", "v4", "v4.01"] 
            #Write pathway for the folder containing the anchorPointFile, you need to figure out your self you can have all the anchorpoints in the same folder as long as the name is different and includes version in the name so you can iterate through all of them
            AnchorpointFile = pd.read_excel(f"C:\\Users\\mats_\\Desktop\\Ebrains\\WHS {vers}\\WHS_SD_rat_atlas_{vers}.nii.xlsx")
                
        #Look through the version innovation document to find the row with matching ID
            findAbbre = VerInnoFile[VerInnoFile["Zero-based index (IDX)"] == int(Id)]
            #A value that increases if the version you are looking at in the version innovation document passes the version you are currently working with
            passedVers = 0
            
            #The versions in the innovation document
            InnoVersions = ["v1","v1.01", "v2", "v3", "v3.01", "v4","v4.01"]
        #Go through all the versions in this look
            for InternalVers in InnoVersions:
                #Create names based on the current version the loop is iterating throuhg
                VersStatus = f"{InternalVers} status"
                VersDes = f"{InternalVers} description"
                #if you have passed the version you are working with in the version innovation document them break the loop
                if passedVers == 1:
                    break         
                #If the version is the same then set equal to one
                if InternalVers == vers:
                    passedVers = 1

                
                #In some cases there might be something wrong with formating of the document so this part will raise a warning and append a text into the error document
                if findAbbre.empty:
                    wn.warn(f"There is something wrong with {Id}, the program is not able to recognize the data on this line")
                    break
                #Find the criteria by finding the status = new
                elif findAbbre[VersStatus].iloc[0]== "new":
                    seperator = '"'
                    VersionDescription =  findAbbre[VersDes].iloc[0]
                    
                    #Remove the First delineated in part.
                    
                    if "First delineated" in VersionDescription:
                        if len(VersionDescription.split(": ")) > 1:
                            VersionDescription = VersionDescription.split(": ")[1]
                    
                    #Replace "" around quotes to '' as in a json document strings are coded with ""
                    
                    if seperator in VersionDescription:
                        seperator = '"'
                        for seperator in VersionDescription:
                            VersionDescription = VersionDescription.replace('"',"'") 

                    
                    #This section is replaces the sources into a longer and more sofisticated version
                    if "[Papp et al., 2014, Neuroimage]" in VersionDescription:
                        VersionDescription = VersionDescription.replace("[Papp et al., 2014, Neuroimage]", "\n- Papp EA, Leergaard TB, Calabrese E, Johnson GA, Bjaalie JG (2014) Waxholm Space atlas of the Sprague Dawley rat brain. NeuroImage 97, 374-386. DOI: https://doi.org/10.1016/j.neuroimage.2014.04.001")
                        
                        
                    if "[Osen et al., 2019, Neuroimage]" in VersionDescription:
                        VersionDescription = VersionDescription.replace("[Osen et al., 2019, Neuroimage]", "\n- Osen KK, Imad J, Wennberg AE, Papp EA, Leergaard TB (2019) Waxholm Space atlas of the rat brain auditory system: Three-dimensional delineations based on structural and diffusion tensor magnetic resonance imaging. NeuroImage 199, 38-56. DOI:")
                        
                        
                    if "[Kjonigsen et al., 2015, Neuroimage]" in VersionDescription:
                        VersionDescription = VersionDescription.replace("[Kjonigsen et al., 2015, Neuroimage]", "\n- Kjonigsen LJ, Lillehaug S, Bjaalie JG, Witter MP, Leergaard TB (2015) Waxholm Space atlas of the rat brain hippocampal region: Three-dimensional delineations based on magnetic resonance and diffusion tensor imaging. NeuroImage 108, 441-449. DOI:")
                        

                    if "From Kjonigsen et al., 2015: " in VersionDescription:
                        VersionDescription = VersionDescription.split("From Kjonigsen et al., 2015: ")[1]
                        VersionDescription = VersionDescription + "\n- Kjonigsen LJ, Lillehaug S, Bjaalie JG, Witter MP, Leergaard TB (2015) Waxholm Space atlas of the rat brain hippocampal region: Three-dimensional delineations based on magnetic resonance and diffusion tensor imaging. NeuroImage 108, 441-449. DOI:"
                        
                    if "From Osen et al., 2019: " in VersionDescription:
                        VersionDescription = VersionDescription.split("From Osen et al., 2019: ")[1]
                        VersionDescription = VersionDescription + "\n- Kjonigsen LJ, Lillehaug S, Bjaalie JG, Witter MP, Leergaard TB (2015) Waxholm Space atlas of the rat brain hippocampal region: Three-dimensional delineations based on magnetic resonance and diffusion tensor imaging. NeuroImage 108, 441-449. DOI:"

                    #Appends to the copied pEV
                    #OpenParcEnt["hasAnnotation"][0] |= {"criteria" : VersionDescription}
                    OpenParcEnt |= {"versionInnovation" : f"First delineated in version {InternalVers}"}
                #If its not new then put in revised if revised and unchanged if unchanged
                if findAbbre[VersStatus].iloc[0]== "revised":

                    OpenParcEnt |= {"versionInnovation" : "revised"}
                    
                elif findAbbre[VersStatus].iloc[0]== "unchanged":

                    OpenParcEnt |= {"versionInnovation" : "unchanged"}
                    
            #find the file that matches the id
            findName = AnchorpointFile[AnchorpointFile["ID"] == int(Id)]
            #if a match that is real and with text then append the anchorpoints
            if len(findName) > 0:
                OpenParcEnt["hasAnnotation"][0] |= {"anchorPoint" : [
        {
        "@type": "https://openminds.ebrains.eu/core/QuantitativeValue",
        "value": float(findName.iloc[0][1])
        },
        {
        "@type": "https://openminds.ebrains.eu/core/QuantitativeValue",
        "value": float(findName.iloc[0][2])
        },
        {
        "@type": "https://openminds.ebrains.eu/core/QuantitativeValue",
        "value": float(findName.iloc[0][3])
        }
    ],}
         
            #convert the dictionary into json format
            newData = json.dumps(OpenParcEnt, indent=2)
            #keep the same name as the file
            keepsamename = datafile.split('\\')
        
            if os.path.isfile(f'C:\\Users\\mats_\\Desktop\\Ebrains\\Visual Code\\openMINDS_SANDS\\instances\\atlas\\parcellationEntity\\WHSSDatlas\\WHSSDatlas_{ParentRegion}.jsonld'):
                meh = 0
            else:
                ("There is no pE for", ParentRegion)
        # open a file with the same name in the destination folder
        with open(f'../openMINDS_SANDS/instances/atlas/parcellationEntityVersion/WHSSDatlas_{vers}/{keepsamename[-1]}', 'w', newline="\n") as file:

            # write the file to destination.
            file.write(newData)
            file.write('\n')
        
            

    