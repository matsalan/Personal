#Importing the required packages
import json
import os
import re
import pandas as pd
from re import sub
from lxml import etree
from bs4 import BeautifulSoup

#Defining the camel case function as many of the links are written in lower camel case
def camel_case(s):
  s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])

#Insert the working directiory
os.chdir("C:\\Users\\mats_\\Desktop\\Ebrains\\Visual Code")
#Define where the label file is located
xmlpath = r"C:\Users\mats_\Desktop\Ebrains\WHS v4.01\MBAT_WHS_SD_rat_atlas_v4.01\Data\WHS_SD_rat_atlas_v4.01_labels.ilf"
#Add where you want the json files to be located.
JsonLocation = r"C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion\WHSSDatlas_v4.01"
#Add where you want the error document to be created 
ErrorLocation = r"C:\Users\mats_\Desktop\Ebrains\Visual Code"

#Write the version of the atlas
VersionIdentity = "v4.01"
#If you want notificatiion and location for each created entity set to = 1
WantNotification = 0

#Variable to check for noparents
NoParent = 0

#Makes a list for the descriptions that are not understood
NoGoodDescription = []
#A variable that checks if the dictonary creation for all the regions are done to create an arror document
ContinueToError = 0
#As ilf files are an xml file i parse them with etree converting it to a form python can work with
root=etree.parse((xmlpath))
#Convert the parsed xml file into a string, which makes the file format way easier to work with.
xmlString = etree.tostring(root)
#Convert it into beautiful soup because it is a wonderful tool.
soup = BeautifulSoup(xmlString)



#Creating a for loop that runs through all the ids below 1000 as these are coded into the atlas
for i in range(0,1000):
  
  #Go through all the columns of data gradually one by one
  val = soup.find(id=i) 
  
  #if i==37:
     #break
  
  #Check if that the ID number is not none, as not all numbers from 1-1000 are represented as ids
  if bool(val) == True:
    #Filter names that have comma and those without, such as Cerebellum, unspecified
    if val["name"].find(",") >= 0:
      #Removed comma
      NameWithComma = val["name"]
      Name = val["name"].replace(",", "")
    #Else continue without any changes
    else:
      Name = val["name"]
      NameWithComma = val["name"]
      
    #Create a lower camelcase version of the name for the links
    CamelName = camel_case(Name)
    
    #Store abbreviation
    Abbre = val["abbreviation"]
    
    #Store id
    Id = val["id"]
    
    #Store Color id
    Color = val["color"]
    
    #Change to uppercase letters as they are in the other versions
    UpperCaseColor = Color.upper()
    
    #This string finds the parent and makes it a string, this is for the HasParent part.
    FoundParent = str(soup.find(id=i).find_parent()).split('<')[1].split('>')[0]
    
    #We need to make an exception for the spinal cord which does not have a parent. This will work for any structure that does not have a parent
    if not FoundParent == "structure":
      ParentRegion = camel_case(FoundParent.split('name="')[1].split('"')[0])
      
    #If there is no parent then update variable used to update the hasParent later                              
    else:
      NoParent = 1   
    
    #Create a dictonary that can be translated to a json file with standard terms and changed links based on the information from the label
    pEV = {
      "@context": {
      "@vocab": "https://openminds.ebrains.eu/vocab/"
        },
      #Change the name of the link to correspond with the new structure
      "@id": f"https://openminds.ebrains.eu/instances/parcellationEntityVersion/WHSSDatlas_{VersionIdentity}_{CamelName}",
      "@type": "https://openminds.ebrains.eu/sands/ParcellationEntityVersion",
      "abbreviation": None,
      "additionalRemarks": None,
      #Insert the abbreviation embedded as an alternate name
      "alternateName": [
        Abbre
        ],
      "correctedName": None,
      "hasAnnotation": [
        {
          "@type": "https://openminds.ebrains.eu/sands/AtlasAnnotation",
          "anchorPoint": None,
          "criteria": None,
          "criteriaQualityType": {
            "@id": "https://openminds.ebrains.eu/instances/criteriaQualityType/processive"
          },
          "criteriaType": {
            "@id": "https://openminds.ebrains.eu/instances/annotationCriteriaType/deterministicAnnotation"
          },
          "inspiredBy": None,
          "internalIdentifier": f"{Id}",
          "laterality": [
            {
              "@id": "https://openminds.ebrains.eu/instances/laterality/left"
            },
            {
              "@id": "https://openminds.ebrains.eu/instances/laterality/right"
            }
          ],
          "preferredVisualization": {
            "@type": "https://openminds.ebrains.eu/sands/ViewerSpecification",
            "additionalRemarks": None,
            "anchorPoint": None,
            "cameraPosition": None,
            "preferredDisplayColor": {
              #Inserts the Color code and updates the link
              "@id": f"https://openminds.ebrains.eu/instances/singleColor/{UpperCaseColor}"
            }
          },
          "specification": None,
          "type": None
        }
      ],
      #Inserts the link to the parent of the region
      "hasParent": [
        {
          "@id": f"https://openminds.ebrains.eu/instances/parcellationEntity/WHSSDatlas_{ParentRegion}"
        }
      ],
        #Changes to include the version identity and the name of the region in camelcase
        "lookupLabel": f"WHSSDatlas_{VersionIdentity}_{CamelName}",
        "name": NameWithComma,
        "ontologyIdentifier": None,
        "relationAssessment": None,
        #Change the version identifier based on the given version
        "versionIdentifier": VersionIdentity,
        "versionInnovation": None
      }
    
    #Updates the dictonary to include the previous named as informed by the description
    if not val.get("description") == None:
      ShortDes = val["description"]
      
      #Looks for previous used description flanked by 'old name' 
      if val["description"].find("'") >= 0:
        AbbreDes = val["description"].split("'")[1].split("'")[0]
        pEV |= {"alternateName" : [
        Abbre, 
        AbbreDes
        ]} 
        AbbreDes = None
        
      #Looks for previous used description between Named old name in and extract old name
      elif val["description"].find("Named ") >=0:
          if val["description"].find(" in") >=0:
            AbbreDes = val["description"].split("Named ")[1].split(" in")[0]
            pEV |= {"alternateName" : [
            Abbre, 
            AbbreDes
            ]} 
            AbbreDes=None
            
          else:
            #If there is something wrong, tell me
            print(f"Unable to understand {ShortDes}, located at id : {Id}")
            
      #Looks for previous used description flanked by (old name)
      elif val["description"].find("(" and ")") >=0:
          AbbreDes = val["description"].split("(")[1].split(")")[0]
          pEV |= {"alternateName" : [
          Abbre, 
          AbbreDes
          ]} 
          AbbreDes=None
          
      elif val["description"].find(f"New in {VersionIdentity}") >= 0:
        #Inserts the description into the versionInnovation if the region is new in this atlas version
        pEV |= {"versionInnovation": val["description"]}
        
      else:
        #If there is something wrong tell me
        print(f"Unable to understand {ShortDes}, located at id : {Id}")
        NoGoodDescription.append(f"Unable to understand {ShortDes}, located at id : {Id}, full line information is: {val}")
    
    if NoParent > 0:
      #Makes sure if there is no parent 
      pEV |= {"hasParent": None}
      NoParent = 0
      
    #Stores the directory as a json file ready for use 
    with open(f'WHSSDatlas_{VersionIdentity}_{CamelName}.json', 'w') as f:
      os.chdir(JsonLocation)
      json.dump(pEV, f, indent=2)
      if WantNotification == 1:
        print("Created", f'WHSSDatlas_{VersionIdentity}_{CamelName}.json', os.getcwd())
        
print("ParcellationEntityVersion json documents are located at", JsonLocation)    
#Prints out the error document
os.chdir(ErrorLocation)
with open('ErrorDocument.txt', 'w') as f:
    for item in NoGoodDescription:
    # write each item on a new line
      f.write("%s\n" % item)
    print("ErrorDocument.txt file is created from list of errors at", os.getcwd())
