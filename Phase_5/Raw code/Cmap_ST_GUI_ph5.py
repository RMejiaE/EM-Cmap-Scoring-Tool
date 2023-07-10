#----------------------------------
#   Developed by:
#   @mcangrejo & @RMejiaE in GitHub
#----------------------------------
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showwarning, showinfo
import webbrowser
import score_trad_ph5 as trad
import networkx as nx
import re
import csv
import os
import copy
#____________Global variable definitions____________#
vGloD_categories = {}
vExtD_wordbank = {}
vGloD_nocategory = {}
vGloD_wordbankcatids = {}  #the keys of the dict are the names of the categories/subactegories, the values are the number of the main category
vGloI_numofcats = 0
vGloM_intercategories = []

#externals
vExtS_rootconcept="Entrepreneurial Mindset"  #String with the root concept, it's changed in the Run button function
vExtL_inputfiles=[]  #List for the concept map files to be scored, it's changed in the Files button function
vExtS_outputfile=''  #String with the path and name of the output file, it's changed in fLoc_outputfile
vExtS_reportfile=''  #String with the path and name of the report file, it's changed in fLoc_outputfile


#___________Widgets instance definitions (Except buttons)______#
#Main window
iTk_main=tk.Tk()     

#Labels
iLabel_frame= ttk.LabelFrame(iTk_main, text = 'Scoring methods')  #label of the frame for the scoring methods
iLabel_rootconcept = ttk.Label(iTk_main, text = 'Root concept:')   #Label for root concept
iLabel_saveas = ttk.Label(iTk_main, text = 'Save results as:')     #Label for saves results as
iLabel_selectmaps = ttk.Label(iTk_main, text = 'Select concept maps:') #Label for select concept maps
iLabel_developers = ttk.Label(iTk_main, text = 'By @mcangrejo & @RMejiaE in GitHub') #Label for developers

#Strings
iString_method = tk.StringVar(value = '0') #String variable to hold the radio button selected. Checked traditional by defaut

#Strings mancatGUI
iString_action = tk.StringVar(value = '1')

#Radio Button
iRadiob_trad = ttk.Radiobutton(iLabel_frame, text = 'Traditional', variable = iString_method, value='1') #checkbox to select traditional method
iRadiob_cat = ttk.Radiobutton(iLabel_frame, text = 'Categorical', variable = iString_method, value='0') #checkbox to select categorical method

#Text Entries
iEntry_rootconcept = ttk.Entry(iTk_main)  #Text Entry for the root concept
iEntry_inputfiles = ttk.Entry(iTk_main)    #Text entry for the input files (disabled by default)
iEntry_outputfile = ttk.Entry(iTk_main) #Text entry for the output file (disabled by default)


#_________________Buttons commands (functions)___________________#

# fLoc_inputfiles opens a file dialog to select the .cxl files to score

def fLoc_inputfiles():
    global vExtL_inputfiles
    vLocS_firstfile=''

    filetypesIn = (
        ('cxl files', '*.cxl'),
        ('All files', '*.*')
    )
    
    vLocT_inputfiles = fd.askopenfilenames(
        title='Select concept maps',
        initialdir=os.getcwd(),
        filetypes=filetypesIn)

    if len(vLocT_inputfiles)>0:

        #vExtL_inputfiles=iTk_main.tk.splitlist(vLocT_inputfiles)    #convert tuple to list if necessary for future dev 
        vExtL_inputfiles=vLocT_inputfiles
       
        vLocS_firstfile=os.path.basename(vExtL_inputfiles[0])
        iEntry_inputfiles.config(state = 'enabled')
        iEntry_inputfiles.delete(0, 'end')                          #it deletes the previous selection

        if len(vLocT_inputfiles)==1:
            iEntry_inputfiles.insert(0,vLocS_firstfile)
        else:
            iEntry_inputfiles.insert(0,vLocS_firstfile + ' + ' + str(len(vExtL_inputfiles)-1) + ' more files')

        iEntry_inputfiles.config(state = 'disabled')
        
#fLoc_outpufile opens a saves as dialog to select the .csv file to save the scoring results     

def fLoc_outputfile():
    global vExtS_outputfile
    global vExtS_reportfile

    filetypesOut = (
        ('csv files', '*.csv'),
        ('All files', '*.*')
    )
    global outfile

    vLocS_outputfile = fd.asksaveasfilename(
        title='Select output file',
        initialdir=os.getcwd(),
        defaultextension='.csv',
        initialfile='ScoringResults.csv',
        filetypes=filetypesOut)

    if len(vLocS_outputfile)>0:
        vExtS_outputfile=vLocS_outputfile
        vExtS_reportfile=os.path.splitext(os.path.basename(vLocS_outputfile))[0] + '_manReport.csv'
        iEntry_outputfile.config(state = 'enabled')
        iEntry_outputfile.delete(0, 'end')
        iEntry_outputfile.insert(0,vExtS_outputfile)
        iEntry_outputfile.config(state = 'disabled')
        

#fLoc_help opens the help window     
def fLoc_help():
    
    try:
        iToplevel_help.deiconify()
        iToplevel_help.protocol('WM_DELETE_WINDOW', lambda: iToplevel_help.withdraw())
        iLabel_helplabel1 = ttk.Label(iToplevel_help, text = str(open('Help.txt',encoding='utf8').read()))
        iLabel_helplabel1.grid(column = 0, row = 0, sticky = tk.EW)
        iButton_detailedhelp = ttk.Button(iToplevel_help, text='Detailed help', command = fLoc_detailedhelp)
        iButton_detailedhelp.grid(column = 0, row = 1)
        iButton_closehelp = ttk.Button(iToplevel_help, text='Close help', command = lambda: iToplevel_help.withdraw())
        iButton_closehelp.grid(column = 0, row = 1, sticky = tk.E)
    except:
        iToplevel_help.withdraw()
        showerror(title = 'Error message:', message = 'Please include the "Help.txt" file in the program folder.\n You may need to download the EM_Cmap_Scoring_Tool_Launcher.zip file and extract the program.\n')


#fLoc_detailedhelp opens the help window
def fLoc_detailedhelp():
    webbrowser.open_new('Help.pdf')

#fLoc_codebook opens the .odf file with the categories descriptions
def fLoc_codebook():
    webbrowser.open_new('Codebook.pdf')
    
#_____________regular functions _____________#

#fLoc_dataextraction extracts the dat from the .cxl file to matrix
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
                  vLocD_conceptsdict[connection[2]]=vLocD_conceptsdict[connection[2]].replace('&#xa;', ' ') #eliminates the line feed character
                  vLocD_conceptsdict[connection[2]]=" ".join(vLocD_conceptsdict[connection[2]].split())  #eliminates leading,ending and duplicated spaces
                  vLocM_toconcept.append (vLocD_conceptsdict[connection[2]].lower())
                  
             # if the linkphrase id in the third position of the connectionsids, it is connecting from a concept       
             if key == connection[2]: 
                 vLocD_conceptsdict[connection[1]]=vLocD_conceptsdict[connection[1]].replace('&#xa;', ' ') #eliminates the line feed character
                 vLocD_conceptsdict[connection[1]]=" ".join(vLocD_conceptsdict[connection[1]].split())  #eliminates leading,ending and duplicated spaces
                 vLocM_fromconcept.append (vLocD_conceptsdict[connection[1]].lower())
          
        for fromconcept in vLocM_fromconcept:   #makes all the possible pair combination
             for  toconcept in vLocM_toconcept:
                vGloM_conceptslinked.append ([fromconcept, toconcept])
    #Check that concepts have at least one connection.
    for pos, concept in enumerate(vGloL_concepts):
        if not any(concept in sub for sub in vGloM_conceptslinked):
            vGloL_concepts.pop(pos)
    return

#fLoc_hiercat attempt to categorize concepts in 'no category' to the category of the first concept of the hierarchy
def fLoc_hiercat(vExtS_rootconcept):
    global vGloD_nocategory
    vLocL_hierarchies=[]
    vLocL_hiercategory=[]   
    
    #empty Multi-directed graph
    G = nx.MultiDiGraph()
    #adds all edges from the list of concepts linked
    G.add_edges_from(vGloM_conceptslinked)
    #creates the list of hierarchies
    vLocL_hierarchies=[x for x in map(str,G.successors(vExtS_rootconcept.lower()))] #to have a list instead of an iterator
    #creates the list of category for the hierarchies
    for hier in vLocL_hierarchies:
        for category, concepts in vGloD_categories.items():
            if hier in concepts:
                vLocL_hiercategory.append(category)

    #iterates over all concepts in No category, calculates to which hierachy concept the path is shorter
    #and assigns it to the corresponding category
    for n in vGloD_categories.get('No category'):
        shortestpath = 0
        assochier = ''
        pathlist = []
        valueslist = []
                
        for index, h in enumerate(vLocL_hierarchies):
            if nx.has_path(G, h, n):
                   pathlist = nx.shortest_path(G, h, n)
                   if shortestpath == 0:          #first iteration for n
                       assoindex= index
                       assochier = h
                       shortestpath = len(pathlist)
                                                                                         
                   else:                           #following iterations for n
                       if (len(pathlist) < shortestpath):
                           assoindex=index
                           assochier = h
                           shortestpath = len(pathlist)

        vGloD_nocategory.get(vLocL_hiercategory[assoindex]).append( n )

#disable_event eliminates the default close of the Mancat GUI window      
def disable_event():
   pass

#fLoc_mancatGUI handles the manual categorization
def fLoc_mancatGUI(vLocS_archivo):
    global vGloD_nocategory
    global vExtD_wordbank
    global vGloD_categories
    global vGloD_wordbankcatids  #the keys of the dict are the names of the categories/subactegories, the values are the number of the main category
    vLocL_categories = []
    vLocL_concepts = []
    vLocM_labelslist = []
    vLocL_action = []
    vLocL_category = []
    vLocL_assignedcat = []
    
    for category in vGloD_nocategory:
        if category != 'No category':
            if vGloD_wordbankcatids[category][0] == vGloD_wordbankcatids[category][1]:
                vLocL_categories.append(category)
            else:
                vLocL_categories.append(' -' + category)
        else:
            vLocL_categories.append(category)
    
    #mancat Toplevel
    iToplevel_mancat = tk.Toplevel(iTk_main)

    iToplevel_mancat.title('Manual Concept Categorization')
    iToplevel_mancat.geometry('650x520+300+50')
    iToplevel_mancat.resizable(1, 1)
    iToplevel_mancat.protocol("WM_DELETE_WINDOW", disable_event)

    #Main frame with scrollbar
    iFrame_mainframe = ttk.Frame(iToplevel_mancat)
    #Description frame
    iFrame_description = ttk.LabelFrame(iToplevel_mancat, text = '')
    iFrame_description.pack(fill = tk.BOTH)
    #Description label
    iLabel_description = ttk.Label(iFrame_description, text = 'The following concepts were not found in the Wordbank.\nThe tool preassigned them to a category and are presented here for your revision.\nFor a definition of each category, please click on the "Codebook" button in the main window.\n')
    iLabel_description.pack(side = tk.TOP)
    iFrame_mainframe.pack(fill = tk.BOTH, expand = True)
    #Canvas
    iCanvas_canvas = tk.Canvas(iFrame_mainframe)
    iCanvas_canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
    #Scrollbar to canvas
    iScrollbar_scroll = ttk.Scrollbar(iFrame_mainframe, orient = 'vertical', command = iCanvas_canvas.yview)
    iScrollbar_scroll.pack(side = tk.RIGHT, fill = tk.Y)
    #Configure canvas
    iCanvas_canvas.configure(yscrollcommand = iScrollbar_scroll.set)
    iCanvas_canvas.bind('<Configure>', lambda e: iCanvas_canvas.configure(scrollregion = iCanvas_canvas.bbox('all'))) #event
    #Frame in canvas
    iFrame_newframe = ttk.Frame(iCanvas_canvas)
    iFrame_newframe.columnconfigure(0, weight = 1)
    iFrame_newframe.columnconfigure(1, weight = 1)
    iFrame_newframe.columnconfigure(2, weight = 1)
    #Add canvas frame to a window in the canvas
    iCanvas_canvas.create_window((0, 0), window = iFrame_newframe, anchor = 'nw')

    #___________Widgets instance definitions______#
    #Frame
    iFrame_columns = ttk.LabelFrame(iFrame_newframe, text = 'File name: ' + vLocS_archivo)
    iFrame_columns.columnconfigure(0, weight = 1)
    iFrame_columns.columnconfigure(1, weight = 1)
    iFrame_columns.columnconfigure(2, weight = 1)
    #Labels    
    iLabel_category = ttk.Label(iFrame_columns, text = 'Concept')
    iLabel_concept = ttk.Label(iFrame_columns, text = 'Preassigned category')
    iLabel_catassign = ttk.Label(iFrame_columns, text = 'New category')
    iLabel_developer = ttk.Label(iToplevel_mancat, text = 'By @mcangrejo & @RMejiaE in GitHub')
    #mancat GUI actions
    #Frames
    iFrame_actions = ttk.LabelFrame(iToplevel_mancat, text = 'Actions')
    iFrame_actions.rowconfigure(0, weight = 1)
    iFrame_actions.rowconfigure(1, weight = 1)
    iFrame_actions.rowconfigure(2, weight = 1)
    
    #mancat buttons
    iButton_ok = ttk.Button(iFrame_actions, text = 'Continue', command = lambda : iToplevel_mancat.destroy())
    #Strings
    iString_action = tk.StringVar(value = '1')
    #Radio Buttons
    iRadiob_reject = ttk.Radiobutton(iFrame_actions, text = 'Reject all assignments and leave all concepts in "No category"', variable = iString_action, value='2')
    iRadiob_manual = ttk.Radiobutton(iFrame_actions, text = 'Accept all assignments', variable = iString_action, value='1')

    #mancat GUI layout
    #Frame
    iFrame_columns.grid(column = 0, row = 0, sticky = tk.N, padx = 5, pady = 5, columnspan = 4)
    #Labels
    iLabel_category.grid(column = 0, row = 0, sticky = tk.N, padx = 5, pady = 5, columnspan = 1)
    iLabel_concept.grid(column = 1, row = 0, sticky = tk.N, padx = 5, pady = 5, columnspan = 1)
    iLabel_catassign.grid(column = 2, row = 0, sticky = tk.N, padx = 5, pady = 5, columnspan = 1)
    iLabel_developer.pack(side = tk.BOTTOM)
    #Buttons
    iButton_ok.grid(column = 0, row = 3, sticky = tk.N, padx = 5, pady = 5)
    #Frames  
    iFrame_actions.pack(side = tk.BOTTOM, expand = True)
    #Radio Buttons
    iString_action.set('1')
    iRadiob_manual.grid(column = 0, row = 0, sticky = tk.N, padx = 5, pady = 5)
    iRadiob_reject.grid(column = 0, row = 1, sticky = tk.N, padx = 5, pady = 5)

    pos = 1
    for category in vGloD_nocategory:
        if len(vGloD_nocategory.get(category)) != 0:
            for concept in vGloD_nocategory.get(category):
                vLocL_assignedcat.append(category)
                vLocL_concepts.append(concept)
                ttk.Label(iFrame_columns, text = concept).grid(column = 0, row = pos, padx = 5, pady = 5, sticky = tk.N)
                ttk.Label(iFrame_columns, text = category).grid(column = 1, row = pos, padx = 5, pady = 5, sticky = tk.N)
                                
                vLocL_category.append( tk.StringVar(iFrame_columns) )
                vLocL_category[pos - 1].set( category )
                ttk.OptionMenu(iFrame_columns, vLocL_category[pos - 1], category, *vLocL_categories).grid(column = 2, row = pos, sticky = tk.N)
                pos += 1       

    
    iTk_main.wait_window(iToplevel_mancat)
    #
    if iString_action.get() == '1':
        for index, concept in enumerate(vLocL_concepts):
            valueslist = []
            if vLocL_category[index] != 'No category':
                vGloD_categories.get(str(vLocL_category[index].get()).replace(' -', '')).append( concept )
                vGloD_categories.get('No category').remove( concept )
            vGloD_nocategory.get(vLocL_assignedcat[index]).remove( concept )
            vGloD_nocategory.get(str(vLocL_category[index].get()).replace(' -', '')).append( concept )
    elif iString_action.get() == '2':
        for index, concept in enumerate(vLocL_concepts):
            vGloD_nocategory.get(vLocL_assignedcat[index]).remove( concept )
            vGloD_nocategory.get('No category').append( concept )
    
    
    
#fExt_catscoring handles the categorical scoring. It used to be an external function but then the mancatGUI couldn't work. We move it to this file        
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
    global vGloD_categories
    global vGloD_nocategory
    global vGloD_wordbankcatids  #the keys of the dict are the names of the categories/subactegories, the values are the number of the main category
       
    vLocL_cat = []
    vLocM_conceptsid = [] 
    vLocI_numcat = 0  #number of categories/subctagories with concepts
    vLocL_NCAT = []   #List of main categories' numbers with concepts
    vLocI_NCAT = 0    #Number of main categories with concepts
    vLocI_numconcepts = 0
    vLocI_interlinks = 0
    vLocF_catscore = 0.0

    vLocD_summary = {}
    global vGloM_intercategories
    vLocI_countintercat = 0
    
    global vGloI_numofcats
    vLocL_tempcolumns = []           

    #___________Extraction of the WordBank information____#
    try:
        with open('WordBank.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for index,row in enumerate(reader):
                if index != 0:
                    templist = [item for item in row if item!='']
                    if len(templist) == 0:
                        break
                    else:
                        vExtD_wordbank[(templist[0], templist[1],templist[2])] = templist[3:len(templist)]
    except:
        return -2

    vGloI_numofcats = 0
    for category in vExtD_wordbank:
        #Adds categories to the wordbancatids. Value are the category and subcategory's numbers
        vGloD_wordbankcatids.update({category[2] : [category [0], category [1]]})
        if category[0] == category[1]:
            vGloI_numofcats += 1
        
        
    
    #__________Opens or creates the result .csv file and writes headers_________#

    try:
        csvfile=open(vExtS_outputfile,'w', newline='')
    except:
        return -1

        
    oLoc_outputfile=csv.writer(csvfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)
    oLoc_outputfile.writerow(vLocL_mainheader)
    oLoc_outputfile.writerow(vLocL_maindata)

#__________Opens or creates the manual categorisation report .csv _________#

    try:
        csvreport=open(vExtS_reportfile,'w', newline='')
    except:
        return -1

        
    oLoc_reportfile=csv.writer(csvreport,delimiter=',',quoting=csv.QUOTE_MINIMAL)
    oLoc_reportfile.writerow(["Categorisation report of concepts not found in the Wordbank file"])
    
    #________________Extraction of all file names__________#
    
    for file in vExtL_inputfiles:
        vLocL_inputnames.append(os.path.basename(file))
           
    #_________Iterates over each cmap file and does the scoring____________________#
    
    for index, cmapfile in enumerate(vExtL_inputfiles):
        #opens the cmap file
        oGlo_cmapfile = open(cmapfile)

        #verifies that file extension is correct .cxl
        if os.path.splitext(vLocL_inputnames[index])[1][1:] == "cxl":

            #writes the name file
            oLoc_outputfile.writerow([''])
            oLoc_outputfile.writerow(['Filename', vLocL_inputnames[index]])
            
            #calls the function that extracts the data from the file
            fLoc_dataextraction(oGlo_cmapfile)
            # close up the cmap file
            oGlo_cmapfile.close()
            
            vLocM_conceptsid = copy.deepcopy(vGloM_conceptslinked)
            
        #if file extension is not .cxl, writes and continues 
        else:
            oLoc_outputfile.writerow([''])
            oLoc_outputfile.writerow(['Filename', vLocL_inputnames[index],'Incorrect file extension'])
            continue
        
        #Checking of concepts and links lists
        if (len(vGloL_concepts) == 0) or (len(vGloM_conceptslinked) == 0):
            oLoc_outputfile.writerow(['No concepts and/or links between concepts found.'])
            continue
        
        #Checking for root concept in map
        elif vGloL_concepts.count(vExtS_rootconcept.lower()) == 0:

            oLoc_outputfile.writerow([vExtS_rootconcept + ' is not a concept in the map'])
            continue
        else:
            #Matrix initiatization for intercategories
            for i in range(vGloI_numofcats):
                vGloM_intercategories.append([])
                for j in range(vGloI_numofcats):
                    if i == j:
                        vGloM_intercategories[i].insert(j, 'x')
                    else:
                        vGloM_intercategories[i].insert(j, 0)

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
                        for word in vExtD_wordbank.get(category):   
                            if concept == word:
                                vLocL_cat.append(concept)
                                vGloL_concepts[vGloL_concepts.index(concept)] = 'C'
                                break                         

                #Updates the dictionary with the concepts in each category
                vGloD_categories.update({category[2] : vLocL_cat})
                #Updates the no category dictionary with the categories/subcategories keys, and empty values
                vGloD_nocategory.update({category[2] : []})
                #reiniiates the list of concepts
                vLocL_cat = []

                       
            #Updates the concepts without category
            for i in range(len(vGloL_concepts)):
                if (vGloL_concepts[i] != 'C') and (vGloL_concepts[i] != vExtS_rootconcept.lower()):
                    vLocL_cat.append(vGloL_concepts[i])
            vGloD_categories.update({'No category' : vLocL_cat})
            vLocL_cat = []
            vGloD_nocategory.update({'No category' : []})

            #calls function hierarchies categorization
            fLoc_hiercat(vExtS_rootconcept)
            
            #calls function manual categorization GUI
            fLoc_mancatGUI(vLocL_inputnames[index])

            #Interlinks matrix update from concept to category number
            vLocL_NCAT = []       #this list will be updated with the category's number that has concepts in it
            vLocI_NCAT = 0
            for j in range(len(vLocM_conceptsid)):   
                for category, concepts in vGloD_categories.items():   #iterates over each category and concepts within it
                    if category != 'No category':                     #only for categries different to no category  
                        if vLocM_conceptsid[j][0] in concepts:        #compares the first pair's concept with the concepts categorized
                            vLocM_conceptsid[j][0]= vGloD_wordbankcatids[category][0]  #replaces the concept with the number of the main category

                            if vGloD_wordbankcatids[category][0] not in vLocL_NCAT:    #if this category's number is not yet in vLocL_NCAT, it adds it up
                                vLocL_NCAT.append(vGloD_wordbankcatids[category][0])

                        if vLocM_conceptsid[j][1] in concepts:        #repeats the search for the second concept in the pair.
                            vLocM_conceptsid[j][1]= vGloD_wordbankcatids[category][0]

                            if vGloD_wordbankcatids[category][0] not in vLocL_NCAT:
                                vLocL_NCAT.append(vGloD_wordbankcatids[category][0])

            # The number of main categories with concepts is the length of vLocL_NCAT
            vLocI_NCAT=len(vLocL_NCAT)
           
            #Writing file name and headers to the report file
            oLoc_reportfile.writerow([''])
            oLoc_reportfile.writerow(['Filename', vLocL_inputnames[index]])
            oLoc_reportfile.writerow(['Approved category:', 'Concepts not found in the wordbank:'])

            # Writing headers into the .csv file
            oLoc_outputfile.writerow(['Categories:', 'Concepts per category:', 'Number of concepts per category:'])

            #Counting the number of categories and concepts
            vLocI_numcat = 0
            vLocI_numconcepts = 0
            for category in vGloD_wordbankcatids:           
                if vGloD_wordbankcatids[category][0] == vGloD_wordbankcatids[category][1]:
                    oLoc_outputfile.writerow([category ,str(vGloD_categories.get(category)).replace(',', ' '), len(vGloD_categories.get(category))])
                    #manual ctaegorisation report
                    oLoc_reportfile.writerow([category ,str(vGloD_nocategory.get(category)).replace(',', ' ')])
                    
                else:
                    oLoc_outputfile.writerow(['  -' +category ,str(vGloD_categories.get(category)).replace(',', ' '), len(vGloD_categories.get(category))])
                    #manual ctaegorisation report
                    oLoc_reportfile.writerow(['  -' +category ,str(vGloD_nocategory.get(category)).replace(',', ' ')])
                    
                if len(vGloD_categories.get(category)):
                    vLocI_numcat += 1                         #Number of categories/subcategories with a concept
                    vLocI_numconcepts += len(vGloD_categories.get(category))

            #Saving in the results and categorisation report.csv the No category concepts list.
            oLoc_outputfile.writerow(['No category' ,str(vGloD_categories.get('No category')).replace(',', ' '), len(vGloD_categories.get('No category'))])
            oLoc_reportfile.writerow(['No category' ,str(vGloD_categories.get('No category')).replace(',', ' ')])

            #Counting the number of interlinks
            vLocI_interlinks = 0
            for i in vLocM_conceptsid:
                if (i[0].isnumeric() and i[1].isnumeric()) and (i[0] != i[1]):
                    vLocI_interlinks += 1
                    vGloM_intercategories[int(i[0]) - 1][int(i[1]) - 1] += 1

            #Save information to the csv file
            oLoc_outputfile.writerow(['Total number of concepts:', vLocI_numconcepts + len(vGloD_categories.get('No category'))])
            oLoc_outputfile.writerow(['Number of categories & subcategories:', vLocI_numcat])
            oLoc_outputfile.writerow(['Number of categorized concepts (NC):', vLocI_numconcepts])
            oLoc_outputfile.writerow(['Number of Main categories (NCAT):', vLocI_NCAT])
            oLoc_outputfile.writerow(['Number of interlinks (NIL):', vLocI_interlinks])

            vLocF_catscore = 0
            if vLocI_numcat > 0:
                vLocF_catscore = (vLocI_numconcepts)*((vLocI_interlinks) / (vLocI_NCAT))
            oLoc_outputfile.writerow(['Categorical Scoring:', round(vLocF_catscore, 1), 'NC*(NIL/NCAT)'])

            #Saves filename and metrics for each file.
            vLocD_summary.update( {vLocL_inputnames[index] : [vLocI_numconcepts, vLocI_NCAT, vLocI_interlinks, round(vLocF_catscore, 1)] } )
            
            #Writes intercategories matrix
            vLocL_tempcolumns = []
            for cat in vExtD_wordbank:
                if cat[0] == cat[1]:
                    vLocL_tempcolumns.append(cat[2])
            oLoc_outputfile.writerow([' '])
            vLocL_tempcolumns.insert(0, ' ')
            oLoc_outputfile.writerows([vLocL_tempcolumns])
            vLocL_tempcolumns.pop(0)

            for pos, row in enumerate(vGloM_intercategories):
                vGloM_intercategories[pos].insert(0, vLocL_tempcolumns[pos])
                oLoc_outputfile.writerows([vGloM_intercategories[pos]])
            #Clears intercategories matrix
            vGloM_intercategories = []

    #Writes summary information in the csv file.
    vLocD_summary
    oLoc_outputfile.writerow([''])
    oLoc_outputfile.writerow(['Scoring Table Summary:'])
    oLoc_outputfile.writerow(['Filename', 'NC', 'CAT', 'NIL', 'Score'])
    for file in vLocD_summary:
        oLoc_outputfile.writerow([file, vLocD_summary.get(file)[0], vLocD_summary.get(file)[1], vLocD_summary.get(file)[2], vLocD_summary.get(file)[3]])

    csvfile.close()
    csvreport.close()
    return 0

#___________Run button method_______________#
        
#fLoc_run runs the scoring   
def fLoc_run():
    global vExtS_rootconcept
    vExtS_rootconcept=iEntry_rootconcept.get()      #gets the root concept on the Entry box into the variable
    iButton_run.config(state = 'disabled')
    iButton_inputfiles.config(state = 'disabled')
    iButton_outputfile.config(state = 'disabled')

    #No root concept
    if not iEntry_rootconcept.get():
        showerror(title = 'Error message:', message = 'Please include a root concept.\n')
    #No input files
    elif not iEntry_inputfiles.get():
        showerror(title = 'Error message:', message = 'Please select the concept maps.\n')
    #No output file
    elif not iEntry_outputfile.get():
        showerror(title = 'Error message:', message = 'Please select the output file.\n')
        
    else:    
        #Traditional
        if (iString_method.get() == '1'): 
            trad.fExt_tradscoring(vExtS_rootconcept,vExtL_inputfiles,vExtS_outputfile)  
            showinfo(title = 'Scoring calculation', message = 'Method: Traditional \n Your results are ready!')

        #Categorical
        else:

            temp = fExt_catscoring(vExtS_rootconcept,vExtL_inputfiles,vExtS_outputfile)
            if temp == -1:
                showerror(title = 'Error message:', message = 'Please close result output file or manual categorisation report file.\n')
            elif temp == -2:
                showerror(title = 'Error message:', message = 'WordBank file not found.\n')
            else:
                showinfo(title = 'Scoring calculation', message = 'Method: Categorical \n Your results are ready!')
        #Delete the output file in case the user runs again with another method 
        iEntry_outputfile.config(state = 'enabled')
        iEntry_outputfile.delete(0, 'end')
        iEntry_outputfile.config(state = 'disabled')

    iButton_run.config(state = 'enabled')
    iButton_inputfiles.config(state = 'enabled')
    iButton_outputfile.config(state = 'enabled')

#____________Buttons definitions_______________#

#main buttons
iButton_inputfiles = ttk.Button(iTk_main,text='Browse',command=fLoc_inputfiles)
iButton_outputfile = ttk.Button(iTk_main,text='Browse',command=fLoc_outputfile)
iButton_help = ttk.Button(iTk_main,text='Help',command=fLoc_help)
iButton_run = ttk.Button(iTk_main,text='Run',command=fLoc_run)
iButton_exit = ttk.Button(iTk_main,text='Exit',command=lambda: iTk_main.destroy())
iButton_codebook = ttk.Button(iTk_main,text='Codebook',command=fLoc_codebook)

#________________Layout_____________________#

#Main window

iTk_main.title('EM Cmap Scoring Tool')
iTk_main.geometry('750x220+250+50')
iTk_main.columnconfigure(0, weight = 1)
iTk_main.columnconfigure(1, weight = 2)
iTk_main.resizable(0,0) #Not resizable

#help window
iToplevel_help = tk.Toplevel(iTk_main) #Help window
iToplevel_help.title('Help')
iToplevel_help.geometry('630x320+320+300')
iToplevel_help.resizable(0,0)
iToplevel_help.withdraw()

#Labels 

iLabel_frame.grid(column = 0, row = 0, sticky = tk.EW, padx = 5, pady = 5, columnspan = 5)
iLabel_rootconcept.grid(column = 0, row = 1, sticky = tk.W, padx = 5, pady = 5)
iLabel_saveas.grid(column = 0, row = 3, sticky = tk.W, padx = 5, pady = 5)
iLabel_selectmaps.grid(column = 0, row = 2, sticky = tk.W, padx = 5, pady = 5)
iLabel_developers.grid(column = 2, row = 5, sticky = tk.W, padx = 5, pady = 5, columnspan = 3)
#Check boxes

iRadiob_trad.grid(column = 0, row = 0, padx = 5, pady = 5)
iRadiob_cat.grid(column = 1, row = 0, padx = 5, pady = 5)

#Text Entries

iEntry_rootconcept.insert(0,"Entrepreneurial Mindset")
iEntry_rootconcept.grid(column = 1, row = 1, sticky = tk.EW, columnspan = 3) 

iEntry_inputfiles.grid(column = 1, row = 2, sticky = tk.EW, columnspan = 3)
iEntry_inputfiles.config(state = 'disabled')

iEntry_outputfile.grid(column = 1, row = 3, sticky = tk.EW, columnspan = 3)
iEntry_outputfile.config(state = 'disabled')

#Buttons

iButton_inputfiles.grid(column = 4, row = 2, padx = 5, pady = 5)
iButton_outputfile.grid(column = 4, row = 3, padx = 5, pady = 5)
iButton_help.grid(column = 0, row = 4, sticky = tk.W , padx = 5, pady = 5)
iButton_run.grid(column = 2, row = 4, padx = 5, pady = 5)
iButton_exit.grid(column = 4, row = 4, padx = 5, pady = 5)
iButton_codebook.grid(column = 0, row = 4, sticky = tk.N , padx = 5, pady = 5)

#________________GUI Loop__________________#

iTk_main.mainloop()
