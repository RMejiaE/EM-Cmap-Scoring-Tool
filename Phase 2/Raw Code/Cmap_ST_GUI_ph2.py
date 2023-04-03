import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showwarning, showinfo
import webbrowser
import score_trad_ph2
import score_cat_ph2
import networkx as nx

#____________Variable definitions____________#

#externals
vExtS_rootconcept="Entrepreneurial Mindset"  #String with the root concept, it's changed in the Run button function
vExtL_inputfiles=[]  #List for the concept map files to be scored, it's changed in the Files button function
vExtS_outputfile=''  #String with the path and name of the output file, it's changed in the Save button function


#___________Widgets instance definitions (Except buttons)______#

iTk_main=tk.Tk()     #Main window

#Labels
iLabel_frame= ttk.LabelFrame(iTk_main, text = 'Scoring methods')  #label of the frame for the scoring methods
iLabel_rootconcept = ttk.Label(iTk_main, text = 'Root concept:')   #Label for root concept
iLabel_saveas = ttk.Label(iTk_main, text = 'Save results as:')     #Label for saves results as
iLabel_selectmaps = ttk.Label(iTk_main, text = 'Select concept maps:') #Label for select concept maps

#Strings
iString_method = tk.StringVar(value = '1') #String variable to hold the radio button selected. Checked traditional by defaut

#Radio Button
iRadiob_trad = ttk.Radiobutton(iLabel_frame, text = 'Traditional', variable = iString_method, value='1') #checkbox to select traditional method
iRadiob_cat = ttk.Radiobutton(iLabel_frame, text = 'Categorical', variable = iString_method, value='0') #checkbox to select categorical method


#Text Entries
iEntry_rootconcept = ttk.Entry(iTk_main)  #Text Entry for the root concept
iEntry_inputfiles = ttk.Entry(iTk_main)    #Text entry for the input files (disabled by default)
iEntry_outputfile = ttk.Entry(iTk_main) #Text entry for the output file (disabled by default)


#_________________Buttons commands (functions)___________________#

# f_inputfiles opens a file dialog to select the .cxl files to score

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
        
#f_outpufile opens a saves as dialog to select the .csv file to save the scoring results     

def fLoc_outputfile():
    global vExtS_outputfile

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
        iEntry_outputfile.config(state = 'enabled')
        iEntry_outputfile.delete(0, 'end')
        iEntry_outputfile.insert(0,vExtS_outputfile)
        iEntry_outputfile.config(state = 'disabled')
        

#f_output opens the save window or pdf file    
def fLoc_help():
    iToplevel_help.deiconify()
    iToplevel_help.protocol('WM_DELETE_WINDOW', lambda: iToplevel_help.withdraw())
    iLabel_helplabel1 = ttk.Label(iToplevel_help, text = str(open('Help.txt').read()))
    iLabel_helplabel1.grid(column = 0, row = 0, sticky = tk.EW)

    iButton_detailedhelp = ttk.Button(iToplevel_help, text='Detailed help', command = fLoc_detailedhelp)
    iButton_detailedhelp.grid(column = 0, row = 1)

    iButton_closehelp = ttk.Button(iToplevel_help, text='Close help', command = lambda: iToplevel_help.withdraw())
    iButton_closehelp.grid(column = 0, row = 1, sticky = tk.E)

def fLoc_detailedhelp():
    webbrowser.open_new('Help.pdf')

#f_run runs the scoring
    
def fLoc_run():
    global vExtS_rootconcept
    vExtS_rootconcept=iEntry_rootconcept.get()      #gets the root concept on the Entry box into the variable

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
            score_trad_ph2.fExt_tradscoring(vExtS_rootconcept.lower(),vExtL_inputfiles,vExtS_outputfile)  
            showinfo(title = 'Scoring calculation', message = 'Method: Traditional \n Your results are ready!')

        #Categorical
        else: 
            score_cat_ph2.fExt_catscoring(vExtS_rootconcept.lower(),vExtL_inputfiles,vExtS_outputfile)
            showinfo(title = 'Scoring calculation', message = 'Method: Categorical \n Your results are ready!')

        #Delete the output file in case the user runs again with another method 
        iEntry_outputfile.config(state = 'enabled')
        iEntry_outputfile.delete(0, 'end')
        iEntry_outputfile.config(state = 'disabled')

        
#____________Buttons definitions_______________#

#Buttons
iButton_inputfiles = ttk.Button(iTk_main,text='Browse',command=fLoc_inputfiles)
iButton_outputfile = ttk.Button(iTk_main,text='Browse',command=fLoc_outputfile)
iButton_help = ttk.Button(iTk_main,text='Help',command=fLoc_help)
iButton_run = ttk.Button(iTk_main,text='Run',command=fLoc_run)
iButton_exit = ttk.Button(iTk_main,text='Exit',command=lambda: iTk_main.destroy())

     
#________________Layout_____________________#

#Main window

iTk_main.title('EM Cmap Scoring Tool')
iTk_main.geometry('750x200+250+100')
iTk_main.columnconfigure(0, weight = 1)
iTk_main.columnconfigure(1, weight = 2)
iTk_main.resizable(0,0) #Not resizable

#help window
iToplevel_help = tk.Toplevel(iTk_main) #Help window
iToplevel_help.title('Help')
iToplevel_help.geometry('620x200+320+340')
iToplevel_help.resizable(0,0)
iToplevel_help.withdraw()

#Labels 

iLabel_frame.grid(column = 0, row = 0, sticky = tk.EW, padx = 5, pady = 5, columnspan = 5)
iLabel_rootconcept.grid(column = 0, row = 1, sticky = tk.W, padx = 5, pady = 5)
iLabel_saveas.grid(column = 0, row = 3, sticky = tk.W, padx = 5, pady = 5)
iLabel_selectmaps.grid(column = 0, row = 2, sticky = tk.W, padx = 5, pady = 5)

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

#________________GUI Loop__________________#

iTk_main.mainloop()
