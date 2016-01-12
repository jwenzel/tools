#!/usr/bin/python
# -*- coding: utf-8 -*-

# pretty error print in python3
from __future__ import print_function

""" 
    Extracts download links (including ISBN numbers) from a SearchResult.csv
    handed out by SpringerLInk. Downloads the corresponding full books.
    (Be sure that you have access to the books you want to download!)

    Uses the springer_download.py by tuxor1337
    https://github.com/tuxor1337/springerdownload
"""

__author__  = 'Jakob Wenzel'
__email__   = 'jakob.wenzel at uni-weimar dot de'
__date__    = '2016-01-08'
__version__ = 1.0

import sys
import os
import csv
from subprocess import call

##{{{ error and usage
def error(message):
    """ Prints error message. """
    print(message, file=sys.stderr)

def usage(message):
    """ Prints message and quits the program. """
    if message:
        print("---------------------------------------------------")
        error(message)
        print("---------------------------------------------------")

    print()
    usage_str = "Usage: " + sys.argv[0]+ " <k> <n> <a_1,b_1> ... <a_k,b_k> "
    error(usage_str)
    print
    print("-----------------------------------------------------------------")
    print("k       - number of pairs")
    print("n       - prime modulus (defines the field of the coefficients)")
    print("a_i,b_i - pair of values which satisfies p(a_i) = b_i")
    print("-----------------------------------------------------------------")
    exit(1)
##}}}

##{{{ main
def main():
    
    # check if file is given
    if not os.path.exists(sys.argv[1]):
        error_str = "File does not exist."
        usage(error_str)

    filename = sys.argv[1]

    with open(filename, 'r') as f:
        with open("updated.csv", 'w') as out:
            f.next() # skip header line
            for line in f:
                updated_line = line.split(',', 9)[8].strip('"')
                if "http://link.springer.com/book/" not in updated_line:
                    continue
                call(['./springer_download.py', '--autotitle', updated_line])

##}}}

if __name__ == '__main__':
    main()
