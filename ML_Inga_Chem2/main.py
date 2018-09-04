#!/usr/bin/env python
__author__ = 'Wim R.M. Cardoen'

import readfile 
import extract 

filename = filename ="orig/data/inga_compounds_and_unpd_in_silico.mgf"
outfile = "inga_out"
printSZ = 10000
arrLines = readfile.readFile(filename)
print("  File '{0}' contains {1} lines".format(filename,len(arrLines)))

pb = extract.ParseBlocks()
mass, name, massabund, blockind = pb.parseArrLines(arrLines, printSZ)
print("  Summary::")
print("    #El in Pep Mass Array:{0}".format(mass.shape[0]))
print("    #El in Ion Array:{0}".format(name.shape[0]))
print("    Dim Mass Abundance Vector:{0}".format(massabund.shape))
print("    Dim Mass BlockID Vector:{0}".format(blockind.shape))

# print("  Store output vectors in '{0}'".format(outfile + ".npz"))
# pb.saveVectors(outfile)

print(mass)

# To read output:
# import numpy as np
# data = np.load('inga_out.npz')
# data.keys()  -> find key_item
# data['key_item']








