#!/usr/bin/env python
__author__ = 'Wim R.M. Cardoen'
import sys

def readFile(filename):
    """
    Function which reads the Original file
    :param filename:
    :return arr: Array of Lines
    """
    try:
        f = open(filename,"r")
        arr = f.readlines()
        f.close()
    except IOError:
        print("  File '{0}' can NOT be read".format(filename))
        sys.exit()

    return arr

if __name__ == "__main__":
    import os
    filename ="orig/data/inga_compounds_and_unpd_in_silico.mgf"
    arrLines = readFile(filename)

    print("File read")
    print("#Lines:{0}".format(len(arrLines)))

    # Check with linux call
    print("#Lines using Linux call:")
    os.system('cat ' + filename + ' | wc -l ')
