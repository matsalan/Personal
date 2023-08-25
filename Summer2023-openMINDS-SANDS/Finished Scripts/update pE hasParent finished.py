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

#I have a copy of the parcellation Entityversions so i have blue print that does not change in case i want to make changes in the code
parcellationEntity = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntity\WHSSDatlas'

#Target destionation for the parcellationEntityVersions should be in the openMINDS SANDS path 
destination = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntity\WHSSDatlas'

#ilf folders
ilffolder = "C:\\Users\\mats_\\Desktop\\Ebrains"

#Write the versions you want to update
versions = ["v1","v1.01", "v2", "v3", "v3.01", "v4", "v4.01"]

#Set the inspired By link
InspiredByLink = "https://www.nitrc.org/frs/?group_id=1081"

#find the list of parcelEntities
parcelJsons = glob.glob(os.path.join(parcellationEntity, '*.jsonld'))  

#Set the path for the folders with different ilf files for the hasParent
xmlpath = f"C:\\Users\\mats_\\Desktop\\Ebrains\\"      
#for loop going through all the ilf files
for vers in tqdm(versions):
    #open the ilf files
    ilfopen = copy.deepcopy(f"{xmlpath}\\WHS {vers}\\WHS_SD_rat_atlas_{vers}_labels.ilf")
    #As ilf files are an xml file i parse them with etree converting it to a form python can work with
    root=etree.parse((ilfopen))
    #Convert the parsed xml file into a string, which makes the file format way easier to work with.
    xmlString = etree.tostring(root)
    #Convert it into beautiful soup because it is a wonderful tool that makes it python readable.
    soup = BeautifulSoup(xmlString)
    
    #for loop going through all ilf lines of individual files
    for i in range(0,2000):
        val = soup.find(id=i) 
        
        #Make sure there is an entry for the iD
        if bool(val) == True:
            
            #for loop going through all the parcellation Entities
            for parcelEntity in parcelJsons:
                
                #open parcellation Entity 
                with open(parcelEntity) as parcelEnt:
                    #load it
                    OpenParcEnt = json.load(parcelEnt)
                    #Find the parent with the find_parent function and then split to find the name between as it is xml coded
                    FoundParent = str(soup.find(id=i).find_parent()).split('<')[1].split('>')[0]
                    #process the name
                    needprocessname = val["name"]
                    if needprocessname.find(",") >= 0:
                        needprocessname = needprocessname.replace(",","")
                    if needprocessname.find("(") >= 0:
                        needprocessname = needprocessname.replace("(","")
                    if needprocessname.find(")") >= 0:
                        needprocessname = needprocessname.replace(")","")
                    if needprocessname.find("-") >= 0:
                        needprocessname = needprocessname.replace("-","")
                    #make it in camel format                   
                    camelname = camel_case(needprocessname)
                    #if there is no hasVersion then:
                    if OpenParcEnt["hasVersion"] is None :
                        #if the parcellationEntity lookupLabel you look at matches the name of the current ilf file you look at
                        if OpenParcEnt["lookupLabel"] == f"WHSSDatlas_{camelname}":
                                    #make sure it actually has a parent
                                    if not FoundParent == "structure":
                                        #process the name
                                        ParentRegion = FoundParent.split('name="')[1].split('"')[0]
                                        if ParentRegion.find(",") >= 0:
                                            ParentRegion = ParentRegion.replace(",","")
                                        if ParentRegion.find("(") >= 0:
                                            ParentRegion = ParentRegion.replace("(","")
                                        if ParentRegion.find(")") >= 0:
                                            ParentRegion = ParentRegion.replace(")","")
                                        if ParentRegion.find("-") >= 0:
                                            ParentRegion = ParentRegion.replace("-","")
                                        #make it camel case
                                        ParentRegion = camel_case(ParentRegion)
                                        
                                        #change the has Parent to the found version 
                                        OpenParcEnt.update({"hasParent" : [{
                                            "@id": f"https://openminds.ebrains.eu/instances/parcellationEntity/WHSSDatlas_{ParentRegion}" 
                                        }]})          
                                        #Save it 
                                        with open(parcelEntity, 'w', newline = "\n") as parcelEnt:
                                            
                                            dump = json.dumps(OpenParcEnt, indent = 2)
                                            parcelEnt.write(dump)
                                            parcelEnt.write('\n')
                                    else:
                                        #if you could not find a parent then
                                        print("there was an error processing parent for: ", camelname, "with this parent name ", FoundParent)
                        else:
                            continue
                    #if there is an hasVersion list
                    else:
                        #go through all the version in the hasVersion
                        for versionEntries in OpenParcEnt["hasVersion"]:
                            #find the correct version and name
                            if versionEntries["@id"].split("/")[-1] == f"WHSSDatlas_{vers}_{camelname}":
                                #Make sure there is a parent
                                if not FoundParent == "structure":
                                    #process name
                                    ParentRegion = FoundParent.split('name="')[1].split('"')[0]
                                    if ParentRegion.find(",") >= 0:
                                        ParentRegion = ParentRegion.replace(",","")
                                    if ParentRegion.find("(") >= 0:
                                        ParentRegion = ParentRegion.replace("(","")
                                    if ParentRegion.find(")") >= 0:
                                        ParentRegion = ParentRegion.replace(")","")
                                    if ParentRegion.find("-") >= 0:
                                        ParentRegion = ParentRegion.replace("-","")
                                    #make name camelcase
                                    ParentRegion = camel_case(ParentRegion)
                                    #update the format to new hasParent
                                    OpenParcEnt.update({"hasParent" : [{
                                        "@id": f"https://openminds.ebrains.eu/instances/parcellationEntity/WHSSDatlas_{ParentRegion}" 
                                    }]})   
                                    #Save        
                                    with open(parcelEntity, 'w', newline = "\n") as parcelEnt:
                                        
                                        dump = json.dumps(OpenParcEnt, indent = 2)
                                        parcelEnt.write(dump)
                                        parcelEnt.write('\n')
                                    
                                else:
                                    continue 
                        
                            #check if ilf line match the hasVersion line at the correct version
                