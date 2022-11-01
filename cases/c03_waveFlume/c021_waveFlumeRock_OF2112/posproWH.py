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


def readWH(dataDirWH,fileWH):
    # timeList contain the time directories with posprocessing
    timeList = jrOF.listTimeDir(dataDirWH)
    timeWH  = []
    dataWH  = []
    for time_txt in timeList:
        dataFileWH=dataDirWH+'/'+time_txt+'/'+fileWH
        jrOF.fileCheck(dataFileWH)
        zData     = jrOF.readOFColumnData(dataFileWH,0)
        alphaData = jrOF.readOFColumnData(dataFileWH,1)
        WH        = alphaData[0]*(zData[1]-zData[0])/2.
        for i in range(1,len(zData)-1):
            dz = (zData[i+1]-zData[i-1])
            WH = WH + dz*alphaData[i]
            timeWH.append(float(time_txt))
            dataWH.append(WH)
    return timeWH,dataWH

if __name__ == "__main__":
    
    sns.set()  # for nice plots : seaborn setup
    print('OpenFoam post-processing')
    print('Wave Flume : Water Height')
    #-----------------------------
    #    write your code below
    #-----------------------------
    #
    # get the path to the working directory
    case_dir = os.getcwd()
    #
    # posprocessing singleGraph 
    dataDirWH0=case_dir+'/postProcessing/singleGraphWH0'
    #dataDirWH3=case_dir+'/postProcessing/singleGraphWH3'
    timeWH0,dataWH0 = readWH(dataDirWH0,'line_alpha.water.xy')
    #timeWH3,dataWH3 = readWH(dataDirWH3,'line_alpha.water.xy')

            

    plt.figure(0)
    plt.plot(timeWH0,dataWH0,linewidth=3,label='probe x=0 m')
    #plt.plot(timeWH3,dataWH3,linewidth=3,label='probe x=3 m')
    plt.xlabel('time [s]',fontsize=14)
    plt.ylabel('height [m]',fontsize=14)
    plt.title('Water height',fontsize=18)
    plt.legend(loc='upper right')
    plt.tight_layout()
    figFile='waterHeight.pdf'
    #plt.savefig(figFile)
    plt.show()
    

