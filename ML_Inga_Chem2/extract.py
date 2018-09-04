#!/usr/bin/env python
__author__ = 'Wim R.M. Cardoen'

import sys
import numpy as np


class ParseBlocks:

    def __init__(self):
        """
        Constructor - Description of the instance variables
          self.numLines       :: number of lines in the file
          self.indexIonBlocks :: python list with (start,end) indices of Ion Blocks
                                 [start1,end1,start2,end2,.... startn,endn]
          self.numIonBlocks   :: number of Ion Blocks i.e. len(self.indexIonBlocks)//2
          self.szIonBlocks    :: number of (mass,abundance) rows in each Ion Block
          --------------------
          self.pepmassArr     :: 1D Numpy Vector with the Peptide Mass (one entry per Ion Block)
          self.nameionArr     :: 1D Numpy Vector with the Name attached to each Ion Block
          self.massabund      :: 2D Numpy Vector containing on each row
                                 a (mass,abundance) entry
          self.blockind       :: 1D Numpy Vector containing the Ion Block Id of the 
                                    same row in self.massabund

        """
        self.numLines = -1
        self.indexIonBlocks = []
        self.numIonBlocks = -1
        self.szIonBlocks = [] 
        # --------------------------
        self.pepmassArr = []
        self.nameionArr = []
        self.massabund = None
        self.blockind  = None

    def findIonBlocks(self, arrLines):
        """
        Method to locate the beginning and the end of each IonBlock
          The indices at odd numbers -> start of block
          The indices at even numbers -> end of block
        :param arrLines:
        :return:
        """
        self.numLines = len(arrLines)
        STR = "IONS"
        for i, line in enumerate(arrLines):
            if STR in line:
                self.indexIonBlocks.append(i)
        if (len(self.indexIonBlocks) % 2) != 0:
            print("  Error in Ion Blocks -> Missing BEGIN or END STATEMENT")
            sys.exit()
        else:
            self.numIonBlocks = len(self.indexIonBlocks)//2
            self.szIonBlocks = np.zeros(self.numIonBlocks)
        return self.indexIonBlocks

    def parseIonBlock(self, arrLines, blockId):
        """
        Method to retrieve the data from 1 Ion Block (i.e. blockId)
        The ION Block:
            startId = 2 * blockId
            endId   = 2 * blockId + 1
            starts at arrLines[startId] i.e. "BEGIN IONS"
            ends at   arrLines[endId]   i.e. "END IONS"
        :param block:
        :return:
        """
        startId = self.indexIonBlocks[2*blockId]
        endId = self.indexIonBlocks[2*blockId+1]
        # Chunk: all lines of a block
        #        without BEGIN IONS & END IONS
        chunk = [line.strip() for line in arrLines[startId+1:endId]]
        numMasses = len(chunk) - 3
        pepmass = float(chunk[0].split("=")[1])
        nameion = chunk[2].split("=")[1] 

        # Retrieve the masses & abundances
        msab = np.zeros((numMasses,2),dtype=np.float64)
        id = 0
        for line in chunk[3:]:
            mass, abund = line.split()
            msab[id, 0] = float(mass)
            msab[id, 1] = float(abund)
            id +=1 
       
        return pepmass, nameion, msab

    def parseArrLines(self, arrLines, printSZ=-1):
        """
        Method which creates the following objects
           a. a Python list pepmassArr (array of pepmasses)
           b. a Python list nameionArr (array containing name of the ion)
           c. a Numpy 1D-Vector with contains #rows for each Ion Block 
              (=> INDEPENDENT CHECKING PURPOSES)
           d. a Numpy 2D-Vector massabund.
              On each row: mass, abundance
           e. a Numpy 1D-Vector blockind
        :param arrLines:REQUIRED
        :param printSZ: [-1] (OPTIONAL)
        :return: None
        """
        self.findIonBlocks(arrLines)
        self.massabund = np.zeros((self.numLines,2))
        self.blockind = []
        istart = 0
        for blockId in range(self.numIonBlocks):
            if blockId % printSZ == 0 and printSZ > 0 :
                print("      Treating Block Id {0:9d}".format(blockId))
            (pepmass,nameion,msab) = self.parseIonBlock(arrLines, blockId) 
            iend = istart + msab.shape[0]
            self.pepmassArr.append(pepmass)
            self.nameionArr.append(nameion) 
            self.szIonBlocks[blockId] = msab.shape[0]
            self.massabund[istart:iend,:] = msab[:,:]
            self.blockind.extend(msab.shape[0]*[blockId])
            istart = iend

        # Convert self.pepmassArr into a Numpy vector
        self.pepmassArr = np.array(self.pepmassArr, dtype=np.float64) 

        # Convert self.nameionArr into a Numpy vector
        self.nameionArr = np.array(self.nameionArr, dtype=np.object) 

        # Rescale self.massabund to its correct size
        self.massabund = self.massabund[:iend, :]

        # Convert self.blockind to a Numpy vector
        self.blockind = np.array(self.blockind,dtype=np.uint32) 

        # Final (security) Check:
        if sum(self.szIonBlocks) != self.massabund.shape[0]:
            print("     ERROR(a) in parseArrLines")
            sys.exit() 

        if self.massabund.shape[0] != self.blockind.shape[0]:
            print("     ERROR(b) in parseArrLines")
            sys.exit() 
        return self.pepmassArr, self.nameionArr, self.massabund, self.blockind

    def saveVectors(self, filename):
        """
        Method to save NumPy Vectors
        :param filename:
        :return: 0
        """
        try:
            massabund = self.massabund
            blockind = self.blockind
            pepmassArr = self.pepmassArr
            nameionArr = self.nameionArr
            np.savez(filename, massabund, blockind, pepmassArr, nameionArr)
            return 0
        except:
            print("     ERROR: Vectors can't be saved to file '{0}".
                  format(filename))
            return -1

    def __del__(self):
        self.numLines = -1
        self.indexIonBlocks = None
        self.numIonBlocks = -1
        self.szIonBlocks = None
        self.massabund = None
        self.blockind = None
        self.pepmassArr = None
        self.nameionArr = None


if __name__ == "__main__":

    import readfile
    filename = filename ="orig/data/inga_compounds_and_unpd_in_silico.mgf"
    #LASTLINE = 213
    LASTLINE=54
    arrLines = readfile.readFile(filename)
   
    print("*** TEST CASE ***")
    print("    File '{0}' contains {1} lines".format(filename,len(arrLines)))
    print("    #Lines considered:{0}".format(LASTLINE))

    print("    TEST INDVIDUAL FUNCTIONS::")
    # Test on the FIRST x blocks
    arrSlice = arrLines[:LASTLINE][:]
    pb = ParseBlocks()

    # Find Index of the Ion Blocks
    indArr = pb.findIonBlocks(arrSlice)
    print("    Indices of the Block Pairs i.e. (Start,End):\n    {0}".format(indArr))
    for i in indArr:
        print("     --> '{0}'".format(arrSlice[i].strip()))
    print("    #Blocks:{0}\n".format(len(indArr)//2))

    # Parse Ion Blocks
    print("    Parsing Ion Blocks:")
    counterMass = []
    for blockID in range(pb.numIonBlocks):
        (pepmass, nameion, msab) = pb.parseIonBlock(arrSlice, blockID)
        print("    Block ID::{0}".format(blockID))
        print("      pepmass:{0}".format(pepmass))
        print("      nameion:'{0}'".format(nameion))
        print("      shape(msab):{0}".format(msab.shape))
        counterMass.append(msab.shape[0])

    print("    Summary:")
    print("      #Entries per Block:{0}".format(counterMass))
    print("      Total #Blocks:{0}".format(sum(counterMass)))

    # All in ONE TEST:
    print("\n    TEST ALL IN ONCE::")
    pb = ParseBlocks()
    pb.parseArrLines(arrSlice)
    print("      Pep Mass Array:\n      {0}".format(pb.pepmassArr))
    print("      Name Ion Array:\n      {0}".format(pb.nameionArr))
    print("      Mass Abundance + Block Index Vectors:")
    for i in range(len(pb.blockind)):
        print("     {0:12f}  {1:12f}   {2:6d}".format(pb.massabund[i,0],
                                         pb.massabund[i,1],pb.blockind[i]))

    # Simple SORTING (pb.massabund)::
    COLID = 0
    print("    Sort Mass ABUNDANCE along column {0}".format(COLID))
    
    ind0 = np.argsort(pb.massabund[:,COLID])
    massabund_sort0 = pb.massabund[ind0]
    blockind_sort0  = pb.blockind[ind0]
    print("    POST-sort::")
    print("      Mass Abundance + Block Index Vectors:")
    for i in range(len(blockind_sort0)):
        print("     {0:12f}  {1:12f}   {2:6d}".format(massabund_sort0[i,0],
                                         massabund_sort0[i,1], blockind_sort0[i]))

    # Save Output as Numpy Vectors
    outfilename = 'extract_output'
    print("    (Test) Vectors to be stored in '{0}'".format(outfilename + ".npz"))
    pb.saveVectors(outfilename)
    print("    Done test")

