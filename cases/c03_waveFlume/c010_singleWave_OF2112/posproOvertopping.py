#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 19:03:07 2022

@author: Julien.Reveillon@coria.fr
"""

## if not already done, download jrOFapplications.py in your case directory
#  in your terminal type:
#  curl -LJO https://raw.githubusercontent.com/JulienReveillon/openfoam-training/main/python/pospro/jrOFapplications.py

import os
import jrOFapplications as jrOF
import seaborn as sns
import matplotlib.pyplot as plt

#
# code - main program
#
if __name__ == "__main__":

    sns.set()  # for nice plots : seaborn setup
    print('OpenFoam post-processing')
    print('Wave overtopping : water volume')
    #-----------------------------
    #    write your code below
    #-----------------------------
    # get the path to the working directory
    case_dir    = os.getcwd()
    #
    # read cells volumes
    cellVol     = jrOF.readOFScalar(case_dir,'V','0')   # read V in dir 0
    Ncells      = len(cellVol)                     # number of cells
    totalVol    = sum(cellVol)                     # total volume of the geometry
    print('number of cells :',Ncells)
    print('total volume :',totalVol)
    #
    # read cells center position
    cellX       = jrOF.readOFScalar(case_dir,'Cx','0') #read Cx in dir 0
    cellZ       = jrOF.readOFScalar(case_dir,'Cz','0') #read Cz in dir 0
    #
    # time directories of the computation
    ltd         = jrOF.listTimeDir(case_dir)  #list of computed times
    ltd         = ltd[1:]                     #do not use the time 0
    #
    #
    ### compute the volume of liquid over and after the obstacle
    #
    # x position of the front of the ostacle :
    xObs        = 2.7
    # z height of the obstacle
    zObs        = 0.4
    #
    # initalize python lists
    time          = []
    liquidXobs    = [] #volume of liquid over and after the obstacle
    liquidXZobs   = [] #volume of liquid behind the obstacle
    for t in ltd:
        volXobs   = 0
        volXZobs  = 0
        alpha = jrOF.readOFScalar(case_dir,'alpha.water',t)
        for i in range (Ncells):
            if cellX[i]>=xObs:
                volXobs = volXobs +alpha[i]*cellVol[i]
                if cellZ[i]<=zObs :
                    volXZobs = volXZobs +alpha[i]*cellVol[i]
         # complete lists for later plots
        time.append(float(t)) # add the floating value of time (t is a string)
        liquidXobs.append(volXobs)
        liquidXZobs.append(volXZobs)

    plt.figure(0)
    plt.plot(time,liquidXobs,linewidth=3,label='over and after obs.')
    plt.plot(time,liquidXZobs,linewidth=3,label='after and below obs.')
    plt.xlabel('time [s]',fontsize=14)
    plt.ylabel('volume [m^3]',fontsize=14)
    plt.title('Overtopping, liquid volume',fontsize=18)
    plt.legend(loc='upper right')
    plt.tight_layout()
    figFile='overtoppingLiqVol.pdf'
    plt.savefig(figFile)
    # plt.show()
