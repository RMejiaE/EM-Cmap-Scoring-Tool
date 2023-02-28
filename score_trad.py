import csv
import os

def f_simpleprinttrad(vExtS_rootconcept,vExtL_inputfiles,vExtS_outputfile):
  
    vLocL_mainheader=['Method','Root concept','Result file path','Result file name','Input files path']
    vLocS_outputpath=os.path.dirname(vExtS_outputfile)
    vLocS_outputname=os.path.basename(vExtS_outputfile)
    vLocS_inputpath=os.path.dirname(vExtL_inputfiles[0])
    vLocL_maindata=['Traditional',vExtS_rootconcept,vLocS_outputpath,vLocS_outputname,vLocS_inputpath]
    vLocL_inputnames=[]
    for file in vExtL_inputfiles:
        vLocL_inputnames.append(os.path.basename(file))    
    
    with open(vExtS_outputfile,'w', newline='') as csvfile:
         oExt_outputfile=csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
         oExt_outputfile.writerow(vLocL_mainheader)
         oExt_outputfile.writerow(vLocL_maindata)
         oExt_outputfile.writerow(['Filenames'])

         for name in vLocL_inputnames:
             oExt_outputfile.writerow([name]) #square brackets are used to put name in a sequence


