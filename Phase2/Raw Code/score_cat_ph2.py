import re
import csv
import os
import json
import copy
###_______global variables declaration_______#
vExtD_wordbank = {}
with open('WordBank.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for index,row in enumerate(reader):
        if index != 0:
            templist = [item for item in row if item!='']
            if len(templist) == 0:
                break
            else:
                vExtD_wordbank[(templist[0], templist[1],templist[2])] = templist[3:len(templist)]

def fLoc_dataextraction(oGlo_file):
    #___________variables list_______________#
    vLocL_idandconcept = []
    vLocD_conceptsdict = {}
    vLocL_idandlink = []
    vLocD_linksdict = {}
    vLocM_connectionsids = []
    vLocM_toconcept = []
    vLocM_fromconcept = []
    vExtD_wordbank = {}

    #__________global variables______________#
    global vGloM_conceptslinked 
    global vGloL_concepts      

    vGloL_concepts=[]
    vGloM_conceptslinked=[]
    
    #____looks within each line of the file for the concepts, linking phrases and connections__________#
    for line in oGlo_file:
        if "concept id=" in line:
              vLocL_idandconcept = re.findall (r'"([^"]*)"', line)
              vLocD_conceptsdict[vLocL_idandconcept[0]] = vLocL_idandconcept[1]
              vGloL_concepts.append(vLocL_idandconcept[1].lower())   #extracts the concepts
              
        if "linking-phrase id=" in line:
              vLocL_idandlink = re.findall (r'"([^"]*)"', line)
              vLocD_linksdict[vLocL_idandlink[0]] = vLocL_idandlink[1]

        if "connection id=" in line:
              vLocM_connectionsids.append(re.findall (r'"([^"]*)"', line))

    #finds all the connections for a linking phrase   
    for key in vLocD_linksdict:
        vLocM_toconcept = []
        vLocM_fromconcept = []
        for connection in vLocM_connectionsids:

             # if the linkphrase id is in the second position of the connectionsids, it is connecting to a concept
             if key == connection[1]: 
                  vLocM_toconcept.append (vLocD_conceptsdict[connection[2]].lower())
                  
             # if the linkphrase id in the third position of the connectionsids, it is connecting from a concept       
             if key == connection[2]: 
                 vLocM_fromconcept.append (vLocD_conceptsdict[connection[1]].lower())
          
        for fromconcept in vLocM_fromconcept:   #makes all the possible pair combination
             for  toconcept in vLocM_toconcept:
                vGloM_conceptslinked.append ([fromconcept, toconcept])
    return

def fExt_catscoring(vExtS_rootconcept,vExtL_inputfiles,vExtS_outputfile):

    #__________________Variables list______________________#
    
    vLocL_mainheader=['Method', 'Root concept', 'Result file path', 'Result file name', 'Input files path']
    vLocS_outputpath=os.path.dirname(vExtS_outputfile)
    vLocS_outputname=os.path.basename(vExtS_outputfile)
    vLocS_inputpath=os.path.dirname(vExtL_inputfiles[0])
    vLocL_maindata=['Categorical', vExtS_rootconcept,vLocS_outputpath, vLocS_outputname, vLocS_inputpath]
    vLocL_inputnames=[]
    global oGlo_file
    vLocI_noroot = 1
    global vExtD_wordbank
    global vGloL_concepts
    global vGloM_conceptslinked
    vLocL_cat = []
    vLocD_categories = {}
    vLocM_conceptsid = [] 
    vLocI_numcat = 0
    vLocI_interlinks = 0
    #________________Extraction of all file names__________#
    for file in vExtL_inputfiles:
        vLocL_inputnames.append(os.path.basename(file))    

    #__________Opens or creates the result .csv file and writes the headers_________#
    csvfile=open(vExtS_outputfile,'w', newline='')
##    oLoc_outputfile=csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
    oLoc_outputfile=csv.writer(csvfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)
    oLoc_outputfile.writerow(vLocL_mainheader)
    oLoc_outputfile.writerow(vLocL_maindata)
    
    #_________Iterates over each cmap file and does the scoring____________________#     
    for index, cmapfile in enumerate(vExtL_inputfiles):

        #opens the cmap file
        oGlo_cmapfile = open(cmapfile)

        #verifies that file extension is correct .cxl
        if os.path.splitext(vLocL_inputnames[index])[1][1:] == "cxl":

            #writes the name file
            oLoc_outputfile.writerow(['Filename', vLocL_inputnames[index]])
            
            #calls the function that extracts the data from the file
            fLoc_dataextraction(oGlo_cmapfile)            
            vLocM_conceptsid = copy.deepcopy(vGloM_conceptslinked)
        #if file extension is not .cxl, writes and continues 
        else:
            oLoc_outputfile.writerow(['Filename', vLocL_inputnames[index],'Incorrect file extension'])
            oGlo_cmapfile.close()
            continue
        #Checking of concepts and links lists
        if (len(vGloL_concepts) == 0) or (len(vGloM_conceptslinked) == 0):
            oLoc_outputfile.writerow(['No concepts and/or links between concepts found.'])
            continue
        #Checking for root conept in map
        elif vGloL_concepts.count(vExtS_rootconcept) == 0:

            oLoc_outputfile.writerow(['No root concept found on concept list'])
            continue
        else:
            #classifying each concept in each category
            for category in vExtD_wordbank:
                for concept in vGloL_concepts:
                    if concept == '???' or concept == '':
                        vGloL_concepts[vGloL_concepts.index(concept)] = ' '
                    #Search for a correspondence between the concept and each category element
                    elif concept == category[2].lower():
                        vLocL_cat.append(concept)
                        vGloL_concepts[vGloL_concepts.index(concept)] = 'C'
                    else:
                        for subcat in vExtD_wordbank.get(category):
                            if concept == subcat:
                                vLocL_cat.append(concept)
                                vGloL_concepts[vGloL_concepts.index(concept)] = 'C'
                                break                         
                #Updates the dictionary with the concepts in each category
                vLocD_categories.update({category[2] : vLocL_cat})
                vLocL_cat = []
            #Updates the concepts without category
            for i in range(len(vGloL_concepts)):
                if (vGloL_concepts[i] != 'C') and (vGloL_concepts[i] != vExtS_rootconcept):
                    vLocL_cat.append(vGloL_concepts[i])
            vLocD_categories.update({'No category' : vLocL_cat})
            vLocL_cat = []
            #Checks for root concepts in the concept list
            for i in vExtD_wordbank.keys():
                for j in range(len(vLocM_conceptsid)): 
                    if vLocM_conceptsid[j][0] == vExtS_rootconcept:
                        vLocM_conceptsid[j][0] = 'R'
                    elif vLocM_conceptsid[j][0] == i:
                        #print(vLocM_conceptsid[j][0])
                        vLocM_conceptsid[j][0] = i[1]
                    else:
                        for subcat in vLocD_categories[i[2]]:
                            if vLocM_conceptsid[j][0] == subcat:
                                #print(vLocM_conceptsid[j][0])
                                vLocM_conceptsid[j][0] = i[0] #[0] for Category, [1] for Subcategory
                    if vLocM_conceptsid[j][1] == i:
                        #print(vLocM_conceptsid[j][1])
                        vLocM_conceptsid[j][1] = i[0] #[0] for Category, [1] for Subcategory
                    else:
                        for subcat in vLocD_categories[i[2]]:
                            if vLocM_conceptsid[j][1] == subcat:
                                #print(vLocM_conceptsid[j][1])
                                vLocM_conceptsid[j][1] = i[0] #[0] for Category, [1] for Subcategory           
            #Save information to the csv file
            oLoc_outputfile.writerow(['Categories:', 'Concepts per category:', 'Number of concepts per category:'])                    
            for category in vLocD_categories:           
                oLoc_outputfile.writerow([category ,str(vLocD_categories.get(category)).replace(',', ' '), len(vLocD_categories.get(category))])
                if category == 'No category':
                    break
                elif len(vLocD_categories.get(category)):
                    vLocI_numcat += 1
            oLoc_outputfile.writerow(['Categories present:', vLocI_numcat])
            vLocI_numcat = 0
            #Counting the number of interlinks
            for i in vLocM_conceptsid:
                if (i[0].isnumeric() and i[1].isnumeric()) and (i[0] != i[1]):
                    #print(i[0] + '=>' + i[1])
                    vLocI_interlinks += 1
            oLoc_outputfile.writerow(['Number of interlinks:', vLocI_interlinks])
            vLocI_interlinks = 0
    csvfile.close()
