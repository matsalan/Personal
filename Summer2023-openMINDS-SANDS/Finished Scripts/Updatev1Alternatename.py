#No longer needed, it is integrated in the v1WHSSatases extraction
import json
import os
import glob
import pprint
keywordList = []
v101files = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion\WHSSDatlas_v1.01'
v1files = r'C:\Users\mats_\Desktop\Ebrains\Visual Code\openMINDS_SANDS\instances\atlas\parcellationEntityVersion\WHSSDatlas_v1'
alterName = []

for v1fil in glob.glob(os.path.join(v1files, '*.jsonld')): #only process .JSON files in folder. 
       
    for v101fil in glob.glob(os.path.join(v101files, '*.jsonld')): #only process .JSON files in folder. 
        
        with open(v1fil, 'r') as v1file, open(v101fil, 'r') as v101file:
            
            # read
            v1data = json.load(v1file)
            v101data = json.load(v101file)
            done = 0
            if v1data["hasAnnotation"][0]["internalIdentifier"] == v101data["hasAnnotation"][0]["internalIdentifier"]:
                alterName = v101data["alternateName"]
    
                    
                v1data.update({"alternateName" : alterName})
                newData = json.dumps(v1data, indent=2)
                done = 1
                print(newData)
                print("hei")
            if done == 1:
                break
            
    
    with open(v1fil, 'w', newline="\n") as file:

        file.write(newData)

            

    