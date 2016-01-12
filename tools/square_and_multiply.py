#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" square_and_multiply.py

    Implementieren Sie den Square-and-Multiply-Algorithmus aus der Vorlesung
    (Foli 81) in Python. Das Programm soll dabei drei Werte x,y,n als
    Kommandozeilenparameter entgegennehmen und
        result = x^y mod n
    nach dem Square-and-Multiply-Algorithmus berechnen. Die Python-Funktion
    pow() darf dabei lediglich zum Quadrieren eines Wertes verwendet werden.
    Nutzen Sie das doctest-Modul von Python, um ihr Programm sinnvolln zu testen
    (siehe Pyhton-Handout).
"""

__author__  = 'Jakob Wenzel'
__email__   = 'jakob.wenzel at uni-weimar dot de'
__date__    = '2015-11-17'
__version__ = 1.0

import os
import sys
import math

"""
>>> import square_and_multiply
>>> square_and_multiply.square_and_multiply_original(5,bin(0),19)
1
>>> square_and_multiply.square_and_multiply_original(0,bin(10),178)
0
>>> square_and_multiply.square_and_multiply_original(19,bin(11),113)
101
>>> square_and_multiply.square_and_multiply_original(-7,bin(17),71)
9
>>> square_and_multiply.square_and_multiply_variant(5,bin(0),19)
1
>>> square_and_multiply.square_and_multiply_variant(0,bin(10),178)
0
>>> square_and_multiply.square_and_multiply_variant(19,bin(11),113)
101
>>> square_and_multiply.square_and_multiply_variant(-7,bin(17),71)
9
>>>
"""

def error(message):
    """ Prints error message and quits the program."""
    sys.stderr.write(message)
    exit(1)


def square_and_multiply_original(bas, exp, mod):
    """
    Computes res = x^y mod n using the standard method

     - base (bas) is either square and multiplied (QM, exp_i = 1) or just square
       (Q, exp_i = 0)
     - IMPORTANT: handle the special case when exp = 0 => res = 1

    """
    if (exp[2] == '0') and (len(exp) == 3):
        return 1

    res = bas
    
    # ignore the first 1 since this leads just to 1^2 * bas
    # => "replace" the first QM by bas
    for i in range(3, len(exp)):
        res = pow(res,2,mod)
        if exp[i] != '0':
            res = (res * bas) % mod

    return res


def square_and_multiply_variant(bas, exp, mod):
    """
    Computes res = x^y mod n using the following method:

     - the base (bas) is squared as often as necessary
     - intermediate multiplication values (res) are multiplied
     - IMPORTANT: handle the special case when exp = 0 => res = 1

    """

    if (exp[2] == '0') and (len(exp) == 3):
        return 1

    res = 1
    
    # reverse order loop starting with least significant bit of exp
    for i in range(len(exp), 2, -1):
        if exp[i-1] != '0':
            res = (res * bas) % mod
        bas = pow(bas,2,mod)

    return res


def main():
    usage_str = "Usage: " + sys.argv[0] + " <Integer (Base)> <Integer"\
                "(Exponent)> <Integer (Modulus)>"

    # as in C: argv[0] is always the program name
    if len(sys.argv) != 4:
        error(usage_str)

    # check whether inputs are valid
    #   first input (bas) can be negative => call isnumeric() only for the
    #   second to the last argument
    if len(sys.argv[1]) > 1:
        if not unicode(sys.argv[1][1:], 'utf-8').isnumeric():
            error_str = "First Argument '" + sys.argv[1] + "' is not valid"
            error(error_str)

    # second/third input must be positive
    for val in sys.argv[2:]:
        if not unicode(val, 'utf-8').isnumeric():
            error_str = "Argument '" + val + "' is not valid"
            error(error_str)


    bas = int(sys.argv[1])

    # exp is stored as a string of the form "0b...."
    # argv[0] = '0', argv[1] = 'b'
    exp = bin(int(sys.argv[2]))
    mod = int(sys.argv[3])

    res = square_and_multiply_original(bas, exp, mod)
    print(res)
    res = square_and_multiply_variant(bas, exp, mod)
    print(res)


# program will not be executed directly if it is imported as a module
if __name__ == '__main__':
    main()

