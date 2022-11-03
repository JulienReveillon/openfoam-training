#!/usr/bin/env python
# PROGRAM-NAME: bmCircularPipe.py
print('x..............................................................x')
print('x...             OpenFOAM - www.foam-u.fr')
print('x..............................................................x')
print('x...             program : bmCircularPipe.py')
print('x...     generate axisymetric circular pipe geometry')
print('x..............................................................x')
print('x...             author  : Julien Reveillon')
print('x...             contact : Julien.Reveillon@coria.fr')
print('x...             date    : October 21, 2015')
print('x..............................................................x')
import math
from   math import cos,sin,pi,ceil
import os.path
import os
import sys

class OpenFoamBlockMeshDictWriter(object):
    # Create a blockMeshDict file with info contained in blockMeshDict_data
    def __init__(self, project_path, blockMeshDict_location, blockMeshDict_data):
        # Arguments
        #    project_path : path to the openFoam project - e.g. $FOAM_RUN/myProject
        #    blockMeshDict_location : location of the blockMeshDict file in the project - e.g. system (since v3.0)
        #    blockMeshDict_data : string array with mesh data

        self._project_path       = project_path
        self._location           = blockMeshDict_location
        self._data               = blockMeshDict_data

        self._bMDfile_lines = []
        self._create_bMDheader()
        self._add_data()
        self._write_data()

    def _create_bMDheader(self):
        # OpenFOAM blockMeshDict file header
        self._bMDfile_lines.append("/*--------------------------------*- C++ -*----------------------------------*\\")
        self._bMDfile_lines.append("| =========                 |                                                 |")
        self._bMDfile_lines.append("| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |")
        self._bMDfile_lines.append("|  \\    /   O peration     | Version:  v3.0+                                 |")
        self._bMDfile_lines.append("|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |")
        self._bMDfile_lines.append("|    \\/     M anipulation  |                                                 |")
        self._bMDfile_lines.append("\*---------------------------------------------------------------------------*/")
        self._bMDfile_lines.append("FoamFile")
        self._bMDfile_lines.append("{")
        self._bMDfile_lines.append("    version     2.0;")
        self._bMDfile_lines.append("    format      ascii;")
        self._bMDfile_lines.append("    class       dictionary;")
        self._bMDfile_lines.append("    object      blockMeshDict;")
        self._bMDfile_lines.append("}")
        self._bMDfile_lines.append("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
        self._bMDfile_lines.append("")

    def _add_data(self):
        # Append the mesh data to the file
        self._bMDfile_lines = self._bMDfile_lines + self._data
        self._bMDfile_lines.append("")
        self._bMDfile_lines.append("// ************************************************************************* //")

    def _write_data(self):
        # write the blockMeshDict file
        path_name = os.path.join(self._project_path, self._location)
        if os.path.exists(path_name):
            print('I... blockMeshDict path : '+path_name)
        else:
            print('E... error : blockMeshDict path '+path_name+' do not exists')
            sys.exit()
        file_bMD = open(os.path.join(path_name, "blockMeshDict"), "w")
        file_bMD.write('\n'.join(self._bMDfile_lines))
        file_bMD.close()
        
class OpenFoamTopoSetDictWriter(object):
    # Create a topoSetDict file 
    def __init__(self, project_path, topoSetDict_location, topoSetDict_data):
        # Arguments
        #    project_path         : path to the openFoam project - e.g. $FOAM_RUN/myProject
        #    topoSetDict_location : location of the topoSetDict file in the project 
        #    topoSetDict_data     : string array with mesh data

        self._project_path       = project_path
        self._location           = topoSetDict_location
        self._data               = topoSetDict_data

        self._tSDfile_lines = []
        self._create_tSDheader()
        self._add_data()
        self._write_data()

    def _create_tSDheader(self):
        # OpenFOAM blockMeshDict file header
        self._tSDfile_lines.append("/*--------------------------------*- C++ -*----------------------------------*\\")
        self._tSDfile_lines.append("| =========                 |                                                 |")
        self._tSDfile_lines.append("| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |")
        self._tSDfile_lines.append("|  \\    /   O peration     | Version:  v2112                                 |")
        self._tSDfile_lines.append("|   \\  /    A nd           | Website:  www.openfoam.com                      |")
        self._tSDfile_lines.append("|    \\/     M anipulation  |                                                 |")
        self._tSDfile_lines.append("\*---------------------------------------------------------------------------*/")
        self._tSDfile_lines.append("FoamFile")
        self._tSDfile_lines.append("{")
        self._tSDfile_lines.append("    version     2.0;")
        self._tSDfile_lines.append("    format      ascii;")
        self._tSDfile_lines.append("    class       dictionary;")
        self._tSDfile_lines.append("    object      topoSetDict;")
        self._tSDfile_lines.append("}")
        self._tSDfile_lines.append("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
        self._tSDfile_lines.append("")

    def _add_data(self):
        # Append the mesh data to the file
        self._tSDfile_lines = self._tSDfile_lines + self._data
        self._tSDfile_lines.append("")
        self._tSDfile_lines.append("// ************************************************************************* //")

    def _write_data(self):
        # write the blockMeshDict file
        path_name = os.path.join(self._project_path, self._location)
        if os.path.exists(path_name):
            print('I... topoSetDict path : '+path_name)
        else:
            print('E... error : topoSetDict path '+path_name+' do not exists')
            sys.exit()
        file_tSD = open(os.path.join(path_name, "topoSetDict"), "w")
        file_tSD.write('\n'.join(self._tSDfile_lines))
        file_tSD.close()
        

class bmDoubleFlapper(object):
	# Constructor
    def __init__(self, TX=2.22, TY=0.8, TZ=0.01, FX=0.02, FY=0.6, layerF=0.02, DX=0.11, DY=0.04, deltaG=0.002, projectPath="."):
        self._TX      = TX       # 
        self._TY      = TY       # 
        self._TZ      = TZ     # 
        self._FX      = FX       # 
        self._FY      = FY       # 
        self._DX      = DX       # 
        self._DY      = DY       #
        self._GX      = FX+2*layerF
        self._GY      = FY+2*layerF
        self._LX      = DX-self._GX/2
        self._LY      = DY-layerF
        self._layerF  = layerF   # 
        self._deltaG  = deltaG   #      
        self._dens    = 1./deltaG 
        self._projectPath = projectPath 
        



    # Define all the vertices in the blockMeshDict file
    def _defineVerticesBox(self):
        #simplify the expressions
        TX = self._TX             # 
        TY = self._TY             #             # 
        TZ = self._TZ
        #
        # 6 vertices
        #
        return [
          (-TX/2,0,-TZ/2),
          ( TX/2,0,-TZ/2),
          ( TX/2,TY,-TZ/2),
          (-TX/2,TY,-TZ/2),
          (-TX/2,0,TZ/2),
          ( TX/2,0,TZ/2),
          ( TX/2,TY,TZ/2),
          (-TX/2,TY,TZ/2)
               ]
               
    def _defineVerticesFlapperL(self):
        #simplify the expressions
        TX = self._TX             # 
        TY = self._TY             # 
        TZ = self._TZ
        FX = self._FX             # 
        FY = self._FY             # 
        DX = self._DX             # 
        DY = self._DY             #
        LX = self._LX             # 
        LY = self._LY             #  
        GX = self._GX             # 
        GY = self._GY             #      
        layerF = self._layerF     # 
          
        #
        # 8 vertices
        #
        return [
          (-TX/2+LX,   LY,-TZ/2),
          (-TX/2+LX+GX,LY,-TZ/2),
          (-TX/2+LX+GX,LY+GY,-TZ/2),
          (-TX/2+LX,   LY+GY,-TZ/2),
          (-TX/2+LX,   LY,TZ/2),
          (-TX/2+LX+GX,LY,TZ/2),
          (-TX/2+LX+GX,LY+GY,TZ/2),
          (-TX/2+LX,   LY+GY,TZ/2)
               ]
               
    def _defineVerticesFlapperR(self):
        #simplify the expressions
        TX = self._TX             # 
        TY = self._TY             # 
        TZ = self._TZ
        FX = self._FX             # 
        FY = self._FY             # 
        DX = self._DX             # 
        DY = self._DY             #
        LX = self._LX             # 
        LY = self._LY             # 
        GX = self._GX             # 
        GY = self._GY             #  
        layerF = self._layerF     # 
        #
        # 8 vertices
        #
        return [
          (TX/2-LX-GX,LY,-TZ/2),
          (TX/2-LX,   LY,-TZ/2),
          (TX/2-LX,   LY+GY,-TZ/2),
          (TX/2-LX-GX,LY+GY,-TZ/2),
          (TX/2-LX-GX,LY,TZ/2),
          (TX/2-LX,   LY,TZ/2),
          (TX/2-LX,   LY+GY,TZ/2),
          (TX/2-LX-GX,LY+GY,TZ/2)
               ]

    # Define all the edges in the blockMeshDict file
    def _defineEdges(self):

        return [
               ]


    # define the blocks
    def _defineBlock(self):
        Nz     = 1
        TNy    = ceil(self._TY*self._dens)
        TNx    = ceil(self._TX*self._dens)
        FNy    = ceil(self._FY*self._dens)
        FNx    = ceil(self._FX*self._dens)
        
        return [
            "    hex (0 1 2 3 4 5 6 7) tank (%i %i %i)     " %(TNx, TNy, Nz) + " simpleGrading (1 1 1)",
            "    hex (8 9 10 11 12 13 14 15) flapperL (%i %i %i) " %(FNx, FNy, Nz) + " simpleGrading (1 1 1)",
            "    hex (16 17 18 19 20 21 22 23) flapperR (%i %i %i) " %(FNx, FNy, Nz) + " simpleGrading (1 1 1)"
               ]

    # define the walls and patches
    def _defineBoundaries(self):
        return [
            "    atmosphere",
            "    {",
            "        type patch;",
            "        faces",
            "        (",
            "            (3 2 6 7)",
            "        );",
            "    }",
            "    vertWall",
            "    {",
            "        type wall;",
            "        faces",
            "        (",
            "            (0 4 7 3)",
            "            (1 5 6 2)",
            "        );",
            "    }",
            "    bottomWall",
            "    {",
            "        type wall;",
            "        faces",
            "        (",
            "            (0 1 5 4)",
            "        );",
            "    }",
            "    frontAndBack",
            "    {",
            "        type empty;",
            "        faces",
            "        (",
            "            (0 1 2 3)",
            "            (4 5 6 7)",
            "        );",
            "    }",
            "    oversetL",
            "    {",
            "        type overset;",
            "        faces",
            "        (",
            "            (8 9 13 12)",
            "            (9 13 14 10)",
            "            (11 10 14 15)",
            "            (8 12 15 11)",
            "        );",
            "    }",
            "    oversetR",
            "    {",
            "        type overset;",
            "        faces",
            "        (",
            "            (16 17 21 20)",
            "            (17 21 22 18)",
            "            (18 22 23 19)",
            "            (19 23 20 16)",
            "        );",
            "    }",
            "    frontAndBackL",
            "    {",
            "        type empty;",
            "        faces",
            "        (",
            "            (8 9 10 11)",
            "            (12 13 14 15)",
            "        );",
            "    }",
            "    frontAndBackR",
            "    {",
            "        type empty;",
            "        faces",
            "        (",
            "            (16 17 18 19)",
            "            (20 21 22 23)",
            "        );",
            "    }",
            "    hole",
            "    {",
            "        type wall;",
            "        faces ();",
            "    }"
                        
               ]



    # toposet : define cellSet background: c0 and mesh around both flappers: c1
    def _defineTopoSet(self):
        #simplify the expressions
        LX      = self._LX             # 
        LY      = self._LY             # 
        DX      = self._DX             # 
        DY      = self._DY             # 
        DZ      = 1        
        FX      = self._FX             # 
        FY      = self._FY             # 
        TX      = self._TX             # 
        TY      = self._TY             #         
        deltaIn = 0.001                # shift inside box
        #
        # 6 vertices
        #
        return [ 
            "actions",
            "(",
            "    {",
            "        name    c0;",
            "        type    cellSet;",
            "        action  new;",
            "        source  regionsToCell;",
            "        insidePoints",            
            "        (",
            "            (0 "+str(deltaIn)+" 0)",
            "        );",
            "    }",
            "\n",
            "    {", 
            "        name    c1;",
            "        type    cellSet;",
            "        action  new;",
            "        source  cellToCell;",
            "        set     c0;",            
            "    }",            
            "\n",
            "    {",
            "        name    c1;",
            "        type    cellSet;",
            "        action  invert;",         
            "    }",       
            "\n",
            "    {",
            "        name    c2;",
            "        type    cellSet;",
            "        action  new;",
            "        source  regionsToCell;",
            "        set     c1;",            
            "        insidePoints",            
            "        (",
            "            ("+str(-TX/2+LX+deltaIn)+" "+str(LY+deltaIn)+" 0)",
            "        );",
            "    }",  
            "\n",
            "    {", 
            "        name    c1;",
            "        type    cellSet;",
            "        action  subtract;",
            "        source  cellToCell;",
            "        set     c2;",            
            "    }",            
            "\n",
            "    {", 
            "        name    box;",
            "        type    cellSet;",
            "        action  new;",
            "        source  cellToCell;",
            "        set     c1;",            
            "    }",            
            "\n",       
            "    {", 
            "        name    box;",
            "        type    cellSet;",
            "        action  add;",
            "        source  cellToCell;",
            "        set     c2;",            
            "    }",            
            "\n",  
            "    {", 
            "        name    box;",
            "        type    cellSet;",
            "        action  subset;",
            "        source  boxToCell;",
            "        boxes",            
            "        (",
            "            ("+str(-TX/2+DX-FX/2)+" "+str(DY)+" -1)("+str(-TX/2+DX+FX/2)+" "+str(DY+FY)+" 1)",
            "            ("+str( TX/2-DX-FX/2)+" "+str(DY)+" -1)("+str( TX/2-DX+FX/2)+" "+str(DY+FY)+" 1)",
            "        );",          
            "    }",            
            "\n",  
            "    {",
            "        name    box;",
            "        type    cellSet;",
            "        action  invert;",         
            "    }", 
            ");",      
            "\n"                    
               ]               

    # write blockMeshDict File
    def writeBlockMeshDict(self):
        verticesArrayB = self._defineVerticesBox()
        verticesArrayL = self._defineVerticesFlapperL()
        verticesArrayR = self._defineVerticesFlapperR()
        blockMeshDict  = []
        blockMeshDict.append('scale 1;\n\n')
        blockMeshDict.append('vertices')
        blockMeshDict.append('(')
        for index, vertex in enumerate(verticesArrayB):
            blockMeshDict.append("    (%e %e %e) " %vertex + "// %i" %index)
        blockMeshDict.append("\n")
        for index, vertex in enumerate(verticesArrayL):
            blockMeshDict.append("    (%e %e %e) " %vertex + "// %i" %(index+8))
        blockMeshDict.append("\n")
        for index, vertex in enumerate(verticesArrayR):
            blockMeshDict.append("    (%e %e %e) " %vertex + "// %i" %(index+16))
        blockMeshDict.append(");\n")
        #
        blockMeshDict.append("blocks")
        blockMeshDict.append("(")
        for block in self._defineBlock():
            blockMeshDict.append(block)
        blockMeshDict.append(");\n")
        #
        blockMeshDict.append("edges")
        blockMeshDict.append("(")
        for edge in self._defineEdges():
            blockMeshDict.append(edge)
        blockMeshDict.append(");\n")
        #
        blockMeshDict.append("boundary")
        blockMeshDict.append("(")
        for boundary in self._defineBoundaries():
            blockMeshDict.append(boundary)
        blockMeshDict.append(");\n")
        #
        blockMeshDict.append("mergePatchPairs")
        blockMeshDict.append("(")
        blockMeshDict.append(");\n")
        #
        file = OpenFoamBlockMeshDictWriter(self._projectPath,
                                  "system",
                                   blockMeshDict)
        #
        print('I... blockMeshDict generated')
        


       
    # write topoSetDict File
    def writeTopoSetDict(self):
        topoSetDict = self._defineTopoSet()
        #
        file = OpenFoamTopoSetDictWriter(self._projectPath,
                                  "system",
                                   topoSetDict)
        #
        print('I... topoSetDict generated')

if __name__ == '__main__':
    foamCaseDir = os.getcwd()  #python script must be executed form OF running directory
    doubleFlapper = bmDoubleFlapper(TX=2.22, TY=0.8, FX=0.02, FY=0.6, layerF=0.02, DX=0.11, DY=0.04, deltaG=0.002, projectPath=foamCaseDir)
    doubleFlapper.writeBlockMeshDict()
    doubleFlapper.writeTopoSetDict()
