#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 19:03:07 2022

@author: reveillo
"""

## if not already done, download jrOFapplications.py in your case directory
#  in your terminal type:
#  curl -LJO https://raw.githubusercontent.com/JulienReveillon/openfoam-training/main/python/pospro/jrOFapplications.py

import os
import jrOFapplications as jrOF
import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == "__main__":
    
    sns.set()  # for nice plots : seaborn setup
    print('OpenFoam post-processing')
    print('Wave overtopping : wave impact')
    #-----------------------------
    #    write your code below
    #-----------------------------
    #
    # get the path to the working directory
    case_dir = os.getcwd()
    #
    # posprocessing files path and names 
    # forcesIncompressible
    dataFileFI=case_dir+'/postProcessing/forcesIncompressible/0/forces.dat'
    # pressure patchIntegrate
    dataFilePI=case_dir+'/postProcessing/patchIntegrate/0/surfaceFieldValue.dat'
          
    timeDataFI       = jrOF.readOFColumnData(dataFileFI,0)
    pressureForcesFI = jrOF.readOFColumnData(dataFileFI,1)
    timeDataPI       = jrOF.readOFColumnData(dataFilePI,0)
    pressureForcesPI = jrOF.readOFColumnData(dataFilePI,1)

    plt.figure(0)
    plt.plot(timeDataFI,pressureForcesFI,linewidth=3,label='forcesIncompressible')
    plt.plot(timeDataPI,pressureForcesPI,'--',linewidth=3,label='patchIntegrate')
    plt.xlabel('time [s]',fontsize=14)
    plt.ylabel('force [N]',fontsize=14)
    plt.title('Water impact force',fontsize=18)
    plt.legend(loc='upper right')
    plt.tight_layout()
    figFile='waterImpactForce.pdf'
    plt.savefig(figFile)
    # plt.show()


