#----------------------------------
#   Developed by:
#   @mcangrejo & @RMejiaE in GitHub
#----------------------------------
import re
import csv
import os
import networkx as nx


def fLoc_dataextraction(oGlo_file):
    
    #___________variables list_______________#
    vLocL_idandconcept = []
    vLocD_conceptsdict = {}
    vLocL_idandlink = []
    vLocD_linksdict = {}
    vLocM_connectionsids = []
    vLocM_toconcept = []
    vLocM_fromconcept = []

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
              vLocL_idandconcept[1]=vLocL_idandconcept[1].replace('&#xa;', ' ')  #eliminates the line feed character
              vLocL_idandconcept[1]=" ".join(vLocL_idandconcept[1].split())   #eliminates leading,ending and duplicated spaces 
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
                  vLocD_conceptsdict[connection[2]]=vLocD_conceptsdict[connection[2]].replace('&#xa;', ' ')  #eliminates the line feed character
                  vLocD_conceptsdict[connection[2]]=" ".join(vLocD_conceptsdict[connection[2]].split())  #eliminates leading,ending and duplicated spaces 
                  vLocM_toconcept.append (vLocD_conceptsdict[connection[2]].lower())
                  
                  
             # if the linkphrase id in the third position of the connectionsids, it is connecting from a concept       
             if key == connection[2]: 
                 vLocD_conceptsdict[connection[1]]=vLocD_conceptsdict[connection[1]].replace('&#xa;', ' ')  #eliminates the line feed character
                 vLocD_conceptsdict[connection[1]]=" ".join(vLocD_conceptsdict[connection[1]].split())  #eliminates leading,ending and duplicated spaces 
                 vLocM_fromconcept.append (vLocD_conceptsdict[connection[1]].lower())
                
          
        for fromconcept in vLocM_fromconcept:   #makes all the possible pair combinations
             for  toconcept in vLocM_toconcept:
                vGloM_conceptslinked.append ([fromconcept, toconcept])

    #Check that concepts have at least one connection.
    for pos, concept in enumerate(vGloL_concepts):
        if not any(concept in sub for sub in vGloM_conceptslinked):
            vGloL_concepts.pop(pos)   #removes unconnected concepts

    return

def fExt_tradscoring(vExtS_rootconcept,vExtL_inputfiles,vExtS_outputfile):

    #__________________Variables list______________________#
    
    vLocL_mainheader=['Method', 'Root concept', 'Result file path', 'Result file name', 'Input files path']
    vLocS_outputpath=os.path.dirname(vExtS_outputfile)
    vLocS_outputname=os.path.basename(vExtS_outputfile)
    vLocS_inputpath=os.path.dirname(vExtL_inputfiles[0])
    vLocL_maindata=['Traditional', vExtS_rootconcept,vLocS_outputpath, vLocS_outputname, vLocS_inputpath]
    vLocL_inputnames=[]
    global oGlo_file
    vLocL_hierarchies=[]
    vLocI_numconcepts=0
    vLocI_numhierarchies=0
    vLocI_highesthier=0
    vLocI_numcrosslinks=0
    vLocI_score=0
    ###
    vLocD_summary = {}

    #________________Extraction of all file names__________#
    for file in vExtL_inputfiles:
        vLocL_inputnames.append(os.path.basename(file))    

    #__________Opens or creates the result .csv file and writes the headers_________#
    
    try:
        csvfile=open(vExtS_outputfile,'w', newline='')
    except:
        return -1

    oLoc_outputfile=csv.writer(csvfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)
    oLoc_outputfile.writerow(vLocL_mainheader)
    oLoc_outputfile.writerow(vLocL_maindata)

    
    #_________Iterates over each cmap file and does the scoring____________________#     
    for index, cmapfile in enumerate(vExtL_inputfiles):
        #____________Variables list____________________________#
        vLocL_paths=[]
        G = nx.MultiDiGraph()  #empty Multi-directed graph
        
        #opens the cmap file
        oGlo_cmapfile = open(cmapfile)        

        #verifies that file extension is correct .cxl
        if os.path.splitext(vLocL_inputnames[index])[1][1:] == "cxl":

            #calls the function that extracts the data from the file
            fLoc_dataextraction(oGlo_cmapfile)
            # close up the cmap file
            oGlo_cmapfile.close()

            #Checking that concepts and concepts link are not empty
            if not vGloL_concepts or not vGloM_conceptslinked:
                oLoc_outputfile.writerow([''])
                oLoc_outputfile.writerow(['Filename', vLocL_inputnames[index],'No concepts and/or links between concepts found'])
                continue

            #Adds all edges from the list of concepts linked 
            G.add_edges_from(vGloM_conceptslinked)

            #verifies that root concept is in the graph
            if vExtS_rootconcept.lower() not in G:
                oLoc_outputfile.writerow([''])
                oLoc_outputfile.writerow(['Filename', vLocL_inputnames[index], vExtS_rootconcept+' is not a concept in the map'])
                continue

            #____________# of concepts, hierachies, # of hierarchies______________#
            
            vLocI_numconcepts=G.number_of_nodes()-1  
            vLocL_hierarchies=[x for x in map(str,G.successors(vExtS_rootconcept.lower()))] #to have a list instead of an iterator
            vLocI_numhierarchies=G.out_degree(vExtS_rootconcept.lower())

            
            #______________________ Concepts in hierachies and Highest hierarchy ________________________#

            #Iterates over the nodes in the graph and include a hierarchie attribute in zero
            for n in G:
                G.nodes[n]['hierarchy']=0

            #Iterates over the first level nodes and assigns to them an unique number 
            vLocI_numhierarchy=1
            for h in vLocL_hierarchies:
               G.nodes[h]['hierarchy'] = vLocI_numhierarchy
               vLocI_numhierarchy += 1

              
            #iterates over the rest of the nodes, calculates to which first-level concept the path
            #is shorter and assigns it to the corresponding hierarchy
            vLocI_highesthier=0   
            for n in G.nodes():
               shortestpath = 0
               assochier = ''
               if n not in vLocL_hierarchies: 
                   pathlist = []
                   for h in vLocL_hierarchies:
                       if nx.has_path(G, h, n):
                           pathlist = nx.shortest_path(G, h, n)
                           if shortestpath == 0:          #first iteration for n
                               assochier = h
                               shortestpath = len(pathlist)
                                                                                                 
                           else:                           #following iterations for n
                               if (len(pathlist) < shortestpath):
                                   assochier = h
                                   shortestpath = len(pathlist)
                                        
                   if assochier:
                       G.nodes[n]['hierarchy'] = G.nodes[assochier]['hierarchy']
                       #loose nodes will keep a hierachy of 0

                       if(len(pathlist)>vLocI_highesthier):
                           vLocI_highesthier=len(pathlist)  #updates highest hierarchy

                               
            #______________________ Crosslinks ________________________#

            #it looks for edges that have nodes from different hierachies
            vLocI_numcrosslinks=0
            for e in G.edges():
                if (G.nodes[e[0]]['hierarchy']!=0) and (G.nodes[e[1]]['hierarchy']!=0):
                   if G.nodes[e[0]]['hierarchy']!= G.nodes[e[1]]['hierarchy']:
                       vLocI_numcrosslinks+=1

            #_______________________ score _____________________________#
            #Score = (NC) + (HH)*5 + (NCL)*10
        
            vLocI_score=vLocI_numconcepts + vLocI_highesthier*5 + vLocI_numcrosslinks*10

            ###
            #Saves filename and score for sumary repotr table.
            vLocD_summary.update( {vLocL_inputnames[index] : [vLocI_numconcepts, vLocI_highesthier, vLocI_numcrosslinks, vLocI_score] } )
                       
            #writes the file name
            oLoc_outputfile.writerow([''])
            oLoc_outputfile.writerow(['Filename', vLocL_inputnames[index]])
            oLoc_outputfile.writerow(['# of concepts', vLocI_numconcepts])
            vGloL_concepts.pop( vGloL_concepts.index(vExtS_rootconcept.lower()) )
            oLoc_outputfile.writerow(['List of concepts', str(vGloL_concepts).replace(',', ' ')])
            oLoc_outputfile.writerow(['Hierachies', vLocL_hierarchies])
            oLoc_outputfile.writerow(['# of hierarchies', vLocI_numhierarchies])
            oLoc_outputfile.writerow(['Highest hierarchy', vLocI_highesthier])
            oLoc_outputfile.writerow(['# of crosslinks', vLocI_numcrosslinks])
            oLoc_outputfile.writerow(['Traditional score', vLocI_score, 'NC+(HH*5)+(NCL*10)'])


        #if file extension is not .cxl, writes and continues 
        else:
            oLoc_outputfile.writerow([''])
            oLoc_outputfile.writerow(['Filename', vLocL_inputnames[index],'Incorrect file extension'])
                     
            continue
    #Writes summary information in the csv file.
    oLoc_outputfile.writerow([''])
    oLoc_outputfile.writerow(['Scoring Table Summary:'])
    oLoc_outputfile.writerow(['Filename', 'NC', 'HH', 'NCL', 'Score'])
    for file in vLocD_summary:
        oLoc_outputfile.writerow([file, vLocD_summary.get(file)[0], vLocD_summary.get(file)[1], vLocD_summary.get(file)[2], vLocD_summary.get(file)[3]])

        
    csvfile.close()
