# -*- coding: utf-8 -*-
"""
THese functions are developped to help with 
some basic posptocessing of OF cases from
the University of Rouen Normandy CFD classes

No fancy Python tricks : basic developments only.

To use these functions : add this file in the directory where you are writing your python postprocessing
and add the following line in your script :

from jrOFapplications import *

Julien.Reveillon@coria.fr
"""

#
# libraries
#
import os, sys, fileinput
#
# functions
#

#-------------------
def fileCheck(file):
    """ 
    Stop script if file absent from the computer
    """
    if not os.path.isfile(file):
        print('File : ',file)
        print('E... '+'no file')
        sys.exit()
        
#-----------------------------        
def listTimeDir(case_dir='.'):
    """
    Create a list of the time directories
    
    Return : 
        timeDir : list of the time directory names (string)
    """
    def is_number_tryexcept(s):
        """ 
        Returns True is string is a float. 
        """
        try:
            float(s)
            return True
        except ValueError:
            return False
    #
    allDir     = os.listdir(case_dir)
    timeDirStr = []
    timeDirFlt = []
    for dir in allDir:
        if is_number_tryexcept(dir):
            timeDirStr.append(dir)
            timeDirFlt.append(float(dir))
    # 
    timeDir = [x for _,x in sorted(zip(timeDirFlt,timeDirStr))]
    #
    return timeDir


#------------------------------------------------
def readOFScalar(case_dir,str_scal,str_time):
    """
    Read a file containing a scalar at time str_time
    
    Arguments :
    case_dir  : directory of the OF case (containing 0, constant, system)
    str_scal  : name of the variable file (b, p, k, epsilon, etc.)
    str_time  : time directoty string
    
    Return    :
    dataScal  : list with the scalar values at each cell of the mesh
    """
    scalarFile = case_dir + "/" + str_time + "/" + str_scal
    fileCheck(scalarFile) # does the file exists ? Stop if not.
    #
    # Init list
    flagRead    = 0
    dataScal    = []
    field       = 'none'
    #
    # Read File
    for line in fileinput.input(scalarFile):
        words = line.split()
        if words:
            if words[0]=='internalField' and field=='none':
                field = 'internalField'
            if words[0]=='boundaryField' and field=='internalField':
                field = 'boundaryField'
            if flagRead == 0 and field=='internalField':
                if words[0]=='(':
                    flagRead = 1
            elif flagRead == 1 and field=='internalField':
                if words[0]==')':
                    flagRead = 0
                else:
                    datum = float(words[0])
                    dataScal.append(datum)
    return dataScal
    
    
#------------------------------------------------
def readOFColumnData(dataFile,nCol):
    """
    Read a file with columns of the format "Data0 Data1 Data2 Data3 etc"
    -> If present, parenthesis will be discarded  (presents when vectors)
    -> If present line beginning with # will be ignored  (presents when comments)
    -> Return the column content
    
    
    Arguments :
    dataFile  : path to the file
    nCol      : column number of the considered data (0=time, etc)
    
    Return    :
    data      : corresponding data of the column nCol
    """
    fileCheck(dataFile) # does the file exists ? Stop if not.
    #
    # Init list
    data        = []
    #
    for line in fileinput.input(dataFile):
        # remove parenthesis if any
        line = line.replace('(', '')
        line = line.replace(')', '') 
        # divide each element of the line into words
        words = line.split()
        if words:  # if there is a line in fact
            if words[0][0]!='#':  #do something only if not comment    
               data.append(float(words[nCol]))    
    #         
    return data

