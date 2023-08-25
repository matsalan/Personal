#Excel reading program
import pandas as pd 
import openpyxl
import numpy as np
import copy
#Set the file path
Hierarchy = pd.read_excel(r'C:\Users\mats_\Desktop\Ebrains\AllanBrain\ABAHier2017.xlsx')
#Write the version number of the hierarchy
version = "2017"

#Set the name file
name = f"Codified hierarchy {version}.xlsx"
#Edit the path to correspond to you computer for where you want it to be stored
path = f"C:\\Users\\mats_\\Desktop\\Ebrains\\Computer generated documents\\{name}"


#Remember to adjust information on excel to not skip anything

#Sets up the data frame and the dictonary for storing hierarchy data
SimplifiedHierarchy = {'id':[], 'name':[], 'hierarchy_level':[]}
SimplifiedHierarchy = pd.DataFrame(SimplifiedHierarchy)
StoredHier = {}


#Run a for loop for all the rows in the excel document
for index, row in Hierarchy.iterrows():
    #Find the first instance if NA in the row and extract the name and ID
    hierarchyColumns = row[3:]
    hierarchyIsNA= np.where(~hierarchyColumns.isna())[0]
    regionId = hierarchyColumns[hierarchyIsNA[-1]]
    regionName = hierarchyColumns[hierarchyIsNA[0]]
     
    #Based on the column create a hierarchy level
    hierarchyLevel = hierarchyIsNA[0]

    #Create a temporary file structure for appending
    SHTemp = {'id':[regionId], 'name':[regionName], 'hierarchy_level':[hierarchyLevel]}
    SHTemp = pd.DataFrame(SHTemp)
    SimplifiedHierarchy = pd.concat([SimplifiedHierarchy, SHTemp], ignore_index= 1)

    LastObject = len(SimplifiedHierarchy)-1
    StoredHier |= {int(SimplifiedHierarchy.iloc[-1,2]) : [SimplifiedHierarchy.iloc[-1,2],SimplifiedHierarchy.iloc[-1,0],SimplifiedHierarchy.iloc[-1,1]]}


    #Make a fake dictionary that does not change each iteration
    RevFakeHier = copy.deepcopy(StoredHier)
    
    #Setup the variables
    NoParent = 0
    Parent = 0
    stopall = 0
    #Find the region one hierarchy above, remove those below the current one and check if you are at top level
    for StoreValue in reversed(RevFakeHier):
        #Check if the stored value is larger ie lower in the hierarchy and check if there is more than one region 
        #in the hierarchy list to make sure the highest regions which have no parents gets no parent
        if StoreValue < SimplifiedHierarchy.iloc[-1,2] and len(StoredHier) != 1:
            
            NoParent = 0
            Parent = StoreValue
            break
        #If the stored value passes the one above, ie there is only one instance in the hierarchy storage.
        #Then check if the stored value is 0 so we can set up the no parent for brain, spinal cord and ear
        elif StoreValue == 1:
            NoParent = 1
           
            break
        #Cuts off the stored value as it we have reached a level that is higher than the previous hierarchy stored region
        elif StoreValue >= SimplifiedHierarchy.iloc[-1,2]:

            if StoreValue > SimplifiedHierarchy.iloc[-1,2]:
                StoredHier.pop(StoreValue)
                
                continue
            #if len(StoredHier) == 1:
                Parent = 1
                continue
            continue
    
    #If there was NoParent then set as None
    if NoParent == 1:
        SimplifiedHierarchy.loc[LastObject, "parent"] = "Basic cell groups and regions"

        SimplifiedHierarchy.loc[LastObject, "parentID"] = 8

    #Otherwise set the parent 
    else:
        SimplifiedHierarchy.loc[LastObject, "parent"] = StoredHier[Parent][2]
        SimplifiedHierarchy.loc[LastObject, "parentID"] = StoredHier[Parent][1]
    
    #SimplifiedHierarchy = SimplifiedHierarchy.loc[LastObject, "parent"]
number = 0
for row in range(len(SimplifiedHierarchy)):
    number = number+1
    SimplifiedHierarchy.loc[number-1, "hierarchyID"] = number

#Save it with a header
SimplifiedHierarchy.to_excel(path, header= ["ID", "Name", "Hierarchy Level", "ParentName", "ParentID ", "HierarchyID"], index=False)
print(f"The Organized Hierarchy called {name} is located at {path}")

