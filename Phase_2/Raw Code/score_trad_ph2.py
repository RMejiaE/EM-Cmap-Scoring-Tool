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
                  #vLocM_toconcept.append ([vLocD_linksdict[key],vLocD_conceptsdict[connection[2]]])
                  vLocM_toconcept.append (vLocD_conceptsdict[connection[2]].lower())
                  
             # if the linkphrase id in the third position of the connectionsids, it is connecting from a concept       
             if key == connection[2]: 
                 #vLocM_fromconcept.append ([vLocD_conceptsdict[connection[1]], vLocD_linksdict[key]])
                 vLocM_fromconcept.append (vLocD_conceptsdict[connection[1]].lower())
          
        for fromconcept in vLocM_fromconcept:   #makes all the possible pair combinations
             for  toconcept in vLocM_toconcept:
                vGloM_conceptslinked.append ([fromconcept, toconcept])

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

    #________________Extraction of all file names__________#
    for file in vExtL_inputfiles:
        vLocL_inputnames.append(os.path.basename(file))    

    #__________Opens or creates the result .csv file and writes the headers_________#
    
    csvfile=open(vExtS_outputfile,'w', newline='')
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

            #Adds all edges from the list of concepts linked 
            G.add_edges_from(vGloM_conceptslinked)

            #verifies that root concept is in the graph
            if vExtS_rootconcept.lower() not in G:
                oLoc_outputfile.writerow(['Filename', vLocL_inputnames[index], vExtS_rootconcept.lower()+' is not a concept in the map.\n'])
                # close up the cmap file
                oGlo_cmapfile.close()
                continue

            #____________# of concepts, hierachies, # of hierarchies, Highest hierarchie______________#
#####ESTO HAY QUE AJUSTARLO!!!!!!!!!!!!!!!!!!!!!!!!!!!

            
            vLocI_numconcepts=len(vGloL_concepts)-1
            vLocL_hierarchies=[x for x in map(str,G.successors(vExtS_rootconcept.lower()))] #to have a list instead of an iterator
            vLocI_numhierarchies=G.out_degree(vExtS_rootconcept.lower())

            #Iterates over all simple paths from root concept to every node
            #And adds them to a list of paths
            for n in G.nodes ():
                for path in nx.all_simple_paths(G, source=vExtS_rootconcept.lower(), target=n):
                    vLocL_paths.append(path)
                    
            #Calculates highest hierarchy as the len of the longest path
            vLocI_highesthier= max(len (x) for x in vLocL_paths) - 1        

            #______________________ Crosslinks ________________________#

            #Iterates over the nodes in the graph and include a hierarchie attribute in zero
            for n in G:
                G.nodes[n]['hierarchy']=0

            #Iterates over the first level nodes and assigns to them an unique number 
            vLocI_numhierarchy=1
            for h in vLocL_hierarchies:
               G.nodes[h]['hierarchy'] = vLocI_numhierarchy
               vLocI_numhierarchy += 1

               print('hierarchy:'+ h + '\tnumber:' + str(G.nodes[h]['hierarchy']))

            #iterates over the rest of the nodes, calculates to which first-level concept the path
            #is shorter and assigns it to the corresponding hierarchy     
            for n in G.nodes():
               shortestpath = 0
               assochier = ''
               if n not in vLocL_hierarchies: 
                   pathlist = []
                   for h in vLocL_hierarchies:
                       if nx.has_path(G, h, n):
                           pathlist = nx.shortest_path(G, h, n)
                           if shortestpath == 0:
                               assochier = h
                               shortestpath = len(pathlist)
                           else:
                               if (len(pathlist) < shortestpath):
                                   assochier = h
                                   shortestpath = len(pathlist)
                                                
                   if assochier:
                        G.nodes[n]['hierarchy'] = G.nodes[assochier]['hierarchy']
                        print('node:\t' + n + '\thierarchy:\t' + str(G.nodes[n]['hierarchy']))
                    #loose nodes will keep a hierachy of 0

            #it looks for edges that have nodes from different hierachies
            for e in G.edges():
                if (G.nodes[e[0]]['hierarchy']!=0) and (G.nodes[e[1]]['hierarchy']!=0):
                   if G.nodes[e[0]]['hierarchy']!= G.nodes[e[1]]['hierarchy']:
                       vLocI_numcrosslinks+=1
                       print (str(e[0]) + ' ---- ' + str(e[1]) + ' hierarchies: ' + str (G.nodes[e[0]]['hierarchy']) + ' ---- ' + str(G.nodes[e[1]]['hierarchy']))
            

### LIMPIAR LOS ENMTERS DE LOS CONCEPTOS!!!!!            

####        #________para depurar durante las pruebas_______#
            print(vLocL_inputnames[index])
            #print('concepts list:')
            #print(vGloL_concepts)
            print('Number of concepts')
            print(vLocI_numconcepts)
            print('----------------------')
            #print('Pairs of concepts linked:')
            #print(vGloM_conceptslinked)
            #print('----------------------')
            print('Number of nodes:')
            print(G.number_of_nodes())
            print('Number of edges:')
            print(G.number_of_edges())
            print('----------------------')
            print('Hierarchies:')
            print(list(vLocL_hierarchies))
            print('Number of hierachies:')
            print(vLocI_numhierarchies)
            print('----------------------')
            #print('Paths')
            #print(list(vLocL_paths))
            print('Highest hierarchy:')    
            print(vLocI_highesthier)
            print('Number of Crosslinks:')    
            print(vLocI_numcrosslinks)


            #writes the file name
            oLoc_outputfile.writerow(['Filename', vLocL_inputnames[index],])
                

        #if file extension is not .cxl, writes and continues 
        else:
            oLoc_outputfile.writerow(['Filename', vLocL_inputnames[index],'Incorrect file extension'])
            # close up the cmap file
            oGlo_cmapfile.close()
            continue
        
        # close up the cmap file
        oGlo_cmapfile.close()

    csvfile.close()
